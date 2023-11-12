from django.conf import settings
from social_django.models import UserSocialAuth
from requests_oauthlib import OAuth1Session
from .models import EducationProgram, Institution


def api_request(params, method):
    usersocialauth = UserSocialAuth.objects.filter(provider='mediawiki').first()
    oauth_token = usersocialauth.extra_data.get('access_token').get('oauth_token')
    oauth_token_secret = usersocialauth.extra_data.get('access_token').get('oauth_token_secret')
    client = OAuth1Session(
        settings.SOCIAL_AUTH_MEDIAWIKI_KEY,
        client_secret=settings.SOCIAL_AUTH_MEDIAWIKI_SECRET,
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret
    )

    url = "https://pt.wikiversity.org/w/api.php"
    if method == "POST":
        return client.post(url, data=params, timeout=4)
    else:
        return client.get(url, params=params, timeout=4)


def get_token():
    params = {
        "action": "query",
        "meta": "tokens",
        "format": "json",
        "formatversion": 2,
    }
    response = api_request(params, "GET").json()
    token = response["query"]["tokens"]["csrftoken"]
    return token


def get_content_of_page():
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": "Utilizador:EPorto_(WMB)/Testes",
        "rvprop": "content",
        "rvlimit": 1,
        "rvdir": "older",
        "format": "json"
    }

    response = api_request(params, "GET")
    print(response.json())


def edit_page(title, text, summary):
    token = get_token()
    params = {
        "action": "edit",
        "title": title,
        "text": text,
        "summary": summary,
        "format": "json",
        "token": token
    }

    response = api_request(params, "POST")
    print(response.json())


def build_states():
    states = dict(settings.STATES)
    text = "__NOTOC____NOEDITSECTION__<templatestyles src=\"WikiConecta/Programas de educação.css\"/>\n" +\
           "{{:WikiConecta/Mapa dos programas de educação brasileiros}}\n{{:WikiConecta/Adicionar programa de educação}}"

    for state, state_name in states.items():
        text += "\n\n" + build_state(state)

    text += "\n"

    return text


def build_state(state):
    states = settings.STATES
    institutions = Institution.objects.filter(state=state)
    number_of_education_programs = EducationProgram.objects.filter(institution__state=state).count()

    if not number_of_education_programs:
        text = "==" + dict(states)[state] + "==\n"
    else:
        text = "==" + dict(states)[state] + "==\n''" + build_number_of_education_programs_phrase(number_of_education_programs) + "\n\n".join([build_institution(institution) for institution in institutions])
    return text


def build_number_of_education_programs_phrase(number_of_education_programs):
    if number_of_education_programs == 1:
        return str(number_of_education_programs) + " programa de educação registrado até o momento''\n"
    else:
        str(number_of_education_programs) + " programas de educação registrados até o momento''\n"


def build_institution(institution):
    education_programs = EducationProgram.objects.filter(institution=institution)
    text = """{{:WikiConecta/Instituição\n""" +\
           """  |instituição = """ + institution.name + """\n"""\
           """  |programas   = \n""" + "\n".join([build_education_program(education_program) for education_program in education_programs]) + """\n}}"""
    return text


def build_education_program(education_program):
    name = education_program.name if education_program.name else ""
    link = education_program.link if education_program.link else ""
    start_date = education_program.start_date.strftime('%Y-%m-%d') if education_program.start_date else ""
    end_date = education_program.end_date.strftime('%Y-%m-%d') if education_program.end_date else ""
    number_students = str(education_program.number_students) if education_program.number_students else ""
    course_type = education_program.get_course_type_display() if education_program.course_type else ""

    text = """    {{:WikiConecta/Programa de educação\n""" +\
           """      |nome_curso        = """ + name + """\n""" +\
           """      |link              = """ + link + """\n""" +\
           """      |data_início       = """ + start_date + """\n""" +\
           """      |data_fim          = """ + end_date + """\n""" +\
           """      |número_estudantes = """ + number_students + """\n""" +\
           """      |modalidade        = """ + course_type + """\n""" + \
           build_professors_fields(list(education_program.professor.all())) + """\n    }}"""
    return text


def build_professors_fields(professors):
    professors_list = []
    for index, item in enumerate(professors):
        if item.username:
            professors_list.append(f"      |docente_{index+1} = [[Utilizador(a):{item.username}|{item.name}]]")
        else:
            professors_list.append(f"      |docente_{index + 1} = {item.name}")
    return "\n".join(professors_list)


def build_mapframe():
    text = "<mapframe width=\"500\" height=\"500\" zoom=\"4\" longitude=\"-55\" latitude=\"-16\" align=\"right\" " +\
           "text=\"'''Programas de Educação Brasileiros'''\">\n" +\
           "{\n" +\
           "  \"type\": \"FeatureCollection\",\n" +\
           "  \"features\": [\n" + build_features() + "\n"\
           "  ]\n" +\
           "}\n" +\
           "</mapframe>"

    return text


def build_features():
    text = []
    institutions = Institution.objects.filter(education_program_institution__institution__isnull=False)
    for institution in institutions:
        number_of_education_programs = EducationProgram.objects.filter(institution=institution).count()
        text.append(f'''    {{ "type": "Feature", "geometry": {{ "type": "Point", "coordinates": [{institution.lon}, {institution.lat}] }}, "properties": {{ "title": "{institution.name}", "description": "{{{{:WikiConecta/Instituição/Descrição no mapa|{institution.id}|{number_of_education_programs}}}}}", "marker-size": "small", "marker-color": "4a51d2", "stroke-width": 0 }} }}''')
    return ",\n".join(text)
