from datetime import datetime
from os.path import dirname, join

import pytest
import scrapy
from city_scrapers_core.constants import BOARD, TENTATIVE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.det_local_development_finance_authority import (
    DetLocalDevelopmentFinanceAuthoritySpider
)

# Shared properties between two different page / meeting types

LOCATION = {
    'name': 'DEGC, Guardian Building',
    'address': '500 Griswold St, Suite 2200, Detroit, MI 48226'
}

TITLE = 'Board of Directors'

test_response = file_response(
    join(dirname(__file__), "files", "det_local_development_finance_authority.html"),
    url='http://www.degc.org/public-authorities/ldfa/'
)
freezer = freeze_time('2018-07-26')
spider = DetLocalDevelopmentFinanceAuthoritySpider()
freezer.start()
parsed_items = [item for item in spider._next_meetings(test_response)]
freezer.stop()


def test_initial_request_count():
    items = list(spider.parse(test_response))
    assert len(items) == 3
    urls = {r.url for r in items if isinstance(r, scrapy.Request)}
    assert urls == {
        'http://www.degc.org/public-authorities/ldfa/fy-2017-2018-meetings/',
        'http://www.degc.org/public-authorities/ldfa/ldfa-fy-2016-2017-meetings/'
    }
    items = [i for i in items if not isinstance(i, scrapy.Request)]
    assert len(items) == 1


# current meeting http://www.degc.org/public-authorities/ldfa/
def test_title():
    assert parsed_items[0]['title'] == TITLE


def test_description():
    assert parsed_items[0]['description'] == ''


def test_start():
    assert parsed_items[0]['start'] == datetime(2018, 10, 23, 9, 30)


def test_end():
    assert parsed_items[0]['end'] is None


def test_id():
    assert parsed_items[0][
        'id'] == 'det_local_development_finance_authority/201810230930/x/board_of_directors'


def test_status():
    assert parsed_items[0]['status'] == TENTATIVE


def test_location():
    assert parsed_items[0]['location'] == LOCATION


def test_source():
    assert parsed_items[0]['source'] == 'http://www.degc.org/public-authorities/ldfa/'


def test_links():
    assert parsed_items[0]['links'] == []


@pytest.mark.parametrize('item', parsed_items)
def test_all_day(item):
    assert item['all_day'] is False


@pytest.mark.parametrize('item', parsed_items)
def test_classification(item):
    assert item['classification'] == BOARD


# # previous meetings e.g. http://www.degc.org/public-authorities/ldfa/fy-2017-2018-meetings/
test_prev_response = file_response(
    join(dirname(__file__), "files", "det_local_development_finance_authority_prev.html"),
    url='http://www.degc.org/public-authorities/ldfa/fy-2017-2018-meetings/'
)
parsed_prev_items = [item for item in spider._parse_prev_meetings(test_prev_response)]
parsed_prev_items = sorted(parsed_prev_items, key=lambda x: x['start'], reverse=True)


def test_request_count():
    requests = list(spider._prev_meetings(test_response))
    urls = {r.url for r in requests}
    assert len(requests) == 2
    assert urls == {
        'http://www.degc.org/public-authorities/ldfa/fy-2017-2018-meetings/',
        'http://www.degc.org/public-authorities/ldfa/ldfa-fy-2016-2017-meetings/'
    }


def test_prev_meeting_count():
    # 2017-2018 page (3 meetings)
    assert len(parsed_prev_items) == 3


def test_prev_title():
    assert parsed_prev_items[0]['title'] == TITLE


def test_prev_description():
    assert parsed_prev_items[0]['description'] == ''


def test_prev_start():
    assert parsed_prev_items[0]['start'] == datetime(2018, 6, 19, 9, 30)


def test_prev_end():
    assert parsed_prev_items[0]['end'] is None


def test_prev_id():
    assert parsed_prev_items[0][
        'id'] == 'det_local_development_finance_authority/201806190930/x/board_of_directors'


def test_prev_status():
    assert parsed_prev_items[0]['status'] == 'passed'


def test_prev_location():
    assert parsed_prev_items[0]['location'] == LOCATION


def test_prev_source():
    assert parsed_prev_items[0][
        'source'] == 'http://www.degc.org/public-authorities/ldfa/fy-2017-2018-meetings/'


def test_prev_links():
    assert parsed_prev_items[1]['links'] == [
        {
            'href': 'http://www.degc.org/wp-content/uploads/12-12-17-LDFA-Board-Meeting-Minutes.pdf',  # noqa
            'title': 'LDFA Special Board Meeting Minutes',
        },
        {
            'href':
                'http://www.degc.org/wp-content/uploads/12-12-17-Special-LDFA-Board-Meeting-Agenda-Only.pdf',  # noqa
            'title': 'LDFA Special Board Meeting Agenda',
        },
    ]


@pytest.mark.parametrize('item', parsed_prev_items)
def test_prev_all_day(item):
    assert item['all_day'] is False


@pytest.mark.parametrize('item', parsed_prev_items)
def test_prev_classification(item):
    assert item['classification'] == BOARD
