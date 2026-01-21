import os
import time
import traceback

import psycopg
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

AT_DB_FIELDS = [
    'registration_number',
    'ethics_status',
    'date_submitted',
    'date_registered',
    'date_last_updated',
    'public_title',
    'scientific_title',
    'universal_trial_number',
    'study_type',
    'description',
    'comparator',
    'control_group',
    'inclusion_criteria',
    'sex',
    'healthy_volunteers',
    'exclusion_criteria',
    'purpose',
    'intervention_allocation',
    'enrolling_procedure',
    'sequence_generation',
    'masking_blinding',
    'intervention_assignment',
    #'other_design_features',
    'phase',
    'endpoint_type',
    'statistical_methods',
    'recruitment_status',
    'summary'
]
AT_DB_ARRAY_FIELDS = [
    'secondary_id',
    'health_condition',
    'condition_category',
    'condition_code',
    'intervention_code',
    'primary_outcome',
    'primary_assessment_method',
    'primary_timepoint',
    'secondary_outcome',
    'secondary_assessment_method',
    'secondary_timepoint'
]
AT_DB_ALTARRAY_FIELDS = [
    'who_mask_blind'
]
AT_DB_CONCAT_FIELDS = [
    'min_age',
    'max_age'
]
AT_PAGE_IDS = [
    '#ctl00_body_CXACTRNUMBER',
    '#ctl00_body_CXETHICSREVIEWTOP',
    '#ctl00_body_CXSUBMITDATE',
    '#ctl00_body_CXAPPROVALDATE',
    '#ctl00_body_CXUPDATEDATE',
    '#ctl00_body_CXSTUDYTITLE',
    '#ctl00_body_CXSCIENTIFICTITLE',
    '#ctl00_body_CXUTRN',
    '#ctl00_body_CXSTUDYTYPE',
    '#ctl00_body_CXINTERVENTIONS',
    '#ctl00_body_CXCOMPARATOR',
    '#ctl00_body_CXCONTROL',
    '#ctl00_body_CXINCLUSIVECRITERIA',
    '#ctl00_body_CXINCLUSIVEGENDER',
    '#ctl00_body_CXHEALTHYVOLUNTEER',
    '#ctl00_body_CXEXCLUSIVECRITERIA',
    '#ctl00_body_CXPURPOSE',
    '#ctl00_body_CXALLOCATION',
    '#ctl00_body_CXCONCEALMENT',
    '#ctl00_body_CXSEQUENCE',
    '#ctl00_body_CXMASKING',
    '#ctl00_body_CXASSIGNMENT',
    '#ctl00_body_CXPHASE',
    '#ctl00_body_CXENDPOINT',
    '#ctl00_body_CXSTATISTICALMETHODS',
    '#ctl00_body_CXRECRUITMENTSTATUS',
    '#ctl00_body_CXSUMMARY'
]
AT_PAGE_ARRAY_IDS = [
    { 'pre': '#ctl00_body_repeater_TXSECONDARYID_ctl', 'post': '_CXSECONDARYID' },
    { 'pre': '#ctl00_body_repeater_TXHEALTHCONDITION_ctl', 'post': '_CXHEALTHCONDITION' },
    { 'pre': '#ctl00_body_repeater_TXCONDITIONCODE_ctl', 'post': '_CXCONDITIONCODE1' },
    { 'pre': '#ctl00_body_repeater_TXCONDITIONCODE_ctl', 'post': '_CXCONDITIONCODE2' },
    { 'pre': '#ctl00_body_repeater_TXINTERVENTIONCODE_ctl', 'post': '_CXINTERVENTIONCODE' },
    { 'pre': '#ctl00_body_repeater_TXPRIMARYOUTCOME_ctl', 'post': '_CXOUTCOME' },
    { 'pre': '#ctl00_body_repeater_TXPRIMARYOUTCOME_ctl', 'post': '_CXASSESSMENTMETHOD' },
    { 'pre': '#ctl00_body_repeater_TXPRIMARYOUTCOME_ctl', 'post': '_CXTIMEPOINT' },
    { 'pre': '#ctl00_body_repeater_TXSECONDARYOUTCOME_ctl', 'post': '_CXOUTCOME' },
    { 'pre': '#ctl00_body_repeater_TXSECONDARYOUTCOME_ctl', 'post': '_CXASSESSMENTMETHOD' },
    { 'pre': '#ctl00_body_repeater_TXSECONDARYOUTCOME_ctl', 'post': '_CXTIMEPOINT' }
]
AT_PAGE_ALTARRAY_IDS = [
    'ctl00_body_CXMASKING'
]
AT_PAGE_CONCAT_IDS = [
    ['#ctl00_body_CXINCLUSIVEMINAGE', '#ctl00_body_CXINCLUSIVEMINAGETYPE'],
    ['#ctl00_body_CXINCLUSIVEMAXAGE', '#ctl00_body_CXINCLUSIVEMAXAGETYPE']
]

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DBNAME = os.getenv("DB_NAME")


def get_page(page_url: str) -> requests.Response:
    time.sleep(2)
    return requests.get(page_url)

def collect_and_upsert(
        trial_soup: BeautifulSoup,
        cursor: psycopg.Cursor,
        conn: psycopg.Connection,
        trial_page_url: str) -> None:
    data_fields: list[str | None] = []
    for p_id_item in AT_PAGE_IDS:
        res = trial_soup.select_one(p_id_item)
        if res is None:
            data_fields.append(res)
        else:
            data_fields.append(res.string)

    array_data_fields = []
    for pa_id_item in AT_PAGE_ARRAY_IDS:
        num = 0
        pa_field_data = []
        while True:
            field_id = '{}{:02d}{}'.format(pa_id_item['pre'], num, pa_id_item['post'])
            res = trial_soup.select_one(field_id)
            if res is None:
                break
            pa_field_data.append(res.string)
            num += 1
        array_data_fields.append(pa_field_data)

    altarray_data_fields = []
    for paa_id_item in AT_PAGE_ALTARRAY_IDS:
        num = 1
        paa_field_data = []
        while True:
            field_id = f'{paa_id_item}{num}'
            res = trial_soup.select_one(field_id)
            if res is None:
                break
            paa_field_data.append(res.string)
            num += 1
        altarray_data_fields.append(paa_field_data)

    concat_data_fields = []
    for id_set in AT_PAGE_CONCAT_IDS:
        pc_field_data = ''
        for id_name in id_set:
            res = trial_soup.select_one(id_name)
            if res is None or res.string is None:
                continue
            pc_field_data += ' ' + res.string
        concat_data_fields.append(pc_field_data)



    try:
        all_field_names = AT_DB_FIELDS + AT_DB_ARRAY_FIELDS + AT_DB_ALTARRAY_FIELDS + AT_DB_CONCAT_FIELDS + ['trial_page_url']
        all_fields = data_fields + array_data_fields + altarray_data_fields + concat_data_fields + [trial_page_url]

        insert_query = "INSERT INTO anzctr_trial({}) VALUES ({}) ON CONFLICT(registration_number) DO UPDATE SET {};".format(
            ', '.join(all_field_names),
            ', '.join(['%s' for i in range(len(all_field_names))]),
            ', '.join([all_field_names[i] + ' = %s' for i in range(1, len(all_field_names))])
            )
        # print(insert_query)
        cursor.execute(insert_query, tuple(all_fields + all_fields[1:]))
        conn.commit()
    except Exception as e:
        print(all_field_names)
        print(all_fields)
        print(len(all_field_names), len(all_fields))
        print(e)
        exit()


def ignore_completed_trials(soup: BeautifulSoup) -> bool:
    try:
        rec_status_tag = soup.select_one("#ctl00_body_CXRECRUITMENTSTATUS")
        if rec_status_tag is None:
            return True
        rec_status = rec_status_tag.string
        if rec_status is None or rec_status.strip() == "Completed":
            return True
        return False
    except Exception:
        print("Couldn't find recruitment status on trial page")
        return True

def scrape_anzctr() -> None:
    try:
        print("Attempting DB connection")
        conn = psycopg.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        with conn.cursor() as cursor:
            # UPDATE EXISTING DATA
            print("Check existing data for updates")
            cursor.execute("""SELECT registration_number, date_last_updated, trial_page_url
                           FROM anzctr_trials WHERE recruitment_status IS DISTINCT FROM 'Completed';""")
            rows = cursor.fetchall()
            for row in rows:
                print("Page: " + row[0], end="\t")
                trial_page_url = row[2]
                trial_page_response = get_page(row[2])
                trial_soup = BeautifulSoup(trial_page_response.text, features="html.parser")

                # Check if trial data has been updated
                update_date_tag = trial_soup.select_one("#ctl00_body_CXUPDATEDATE")
                if update_date_tag is None:
                    print("--> Not found")
                    continue
                update_date = update_date_tag.string
                if update_date is None or update_date == row[1]:
                    print("--> No update")
                    continue

                collect_and_upsert(trial_soup, cursor, conn, row[2])
                print("--> Updated")

            print("Update done\n")

            # CHECK FOR NEW DATA
            print("Get crawled page sets")
            cursor.execute("SELECT name, href FROM anzctr_set;")
            rows = cursor.fetchall()
            crawled_sets: dict[str, str] = dict(rows)

            print("Begin crawl")
            main_page_response = get_page("https://www.anzctr.org.au/crawl.aspx")
            main_soup = BeautifulSoup(main_page_response.text, features="html.parser")
            trial_sets_list = [{'text': item.string, 'href': item.attrs['href']} for item in main_soup.select('div.static-content a')]
            for trial_set in trial_sets_list:
                try:
                    trial_set_text = trial_set['text']
                    print(f"Crawling page set: {trial_set_text}")
                    if trial_set_text in crawled_sets:
                        continue
                    trial_set_url = 'https://www.anzctr.org.au{}'.format(trial_set['href'])
                    trial_set_page_response = get_page(trial_set_url)
                    trial_set_soup = BeautifulSoup(trial_set_page_response.text, features="html.parser")
                    trials_list = [
                        {'text': item.string, 'href': item.attrs['href']} for item in trial_set_soup.select('div.static-content a')
                        ]
                    for trial in trials_list:
                        print("Page: {}".format(trial['text']))
                        trial_page_url = 'https://www.anzctr.org.au{}'.format(trial['href'])
                        trial_page_response = get_page(trial_page_url)
                        trial_soup = BeautifulSoup(trial_page_response.text, features="html.parser")
                        if ignore_completed_trials(trial_soup):
                            continue

                        collect_and_upsert(trial_soup, cursor, conn, trial_page_url)

                    insert_query = """INSERT INTO anzctr_set(name, href) VALUES (%s, %s)
                        ON CONFLICT(name) DO NOTHING;"""
                    cursor.execute(insert_query, (trial_set_text, trial_set_url))
                    conn.commit()
                except Exception as error:
                    print('Error: ', error)
                    print(traceback.format_exc())
                    break
            print("Crawl done")
        conn.close()
    except Exception as error:
        print('Error: ', error)

def main() -> None:
    scrape_anzctr()

if __name__ == "__main__":
    main()