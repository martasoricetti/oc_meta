from datetime import datetime
import re
from oc_meta.run.meta_process import MetaProcess, run_meta_process
from ramose import APIManager
from test.curator_test import reset_server
from test.meta_process_test import delete_output_zip
import json
import os
import shutil
import unittest


CONFIG = 'api/oc_meta_v1.hf'
api_manager = APIManager([CONFIG])
api_base = 'http://127.0.0.1:8080/api/v1'

class test_API(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        now = datetime.now()
        reset_server()
        meta_process = MetaProcess(config=os.path.join('test', 'api_test', 'meta_config.yaml'))
        run_meta_process(meta_process)
        shutil.rmtree(meta_process.base_output_dir)
        delete_output_zip('.', now)

    def test_metadata(self):
        operation_url = 'metadata'
        request = 'doi:10.1007/978-1-4020-9632-7__doi:10.1088/0022-3727/39/14/017'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 meta:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
            },
            {
                "id": "doi:10.1088/0022-3727/39/14/017 meta:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
                "date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266]",
                "editor": ""
            }
        ]
        format_expected = 'application/json'
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:x['date']), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:x['date'])
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_metadata_two_schemes(self):
        operation_url = 'metadata'
        request = 'doi:10.1007/978-1-4020-9632-7__issn:0022-3727'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 meta:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
            },
            {
                "id": "issn:0022-3727 meta:br/0604",
                "title": "Journal Of Physics D: Applied Physics",
                "author": "",
                "date": "",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "journal",
                "publisher": "",
                "editor": ""
            }
        ]
        format_expected = 'application/json'
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:x['date']), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:x['date'])
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_metadata_two_schemes_and_metaid(self):
        operation_url = 'metadata'
        request = 'doi:10.1007/978-1-4020-9632-7__issn:0022-3727__meta:br/0602'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 meta:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
                "date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266]",
                "editor": ""
            },
            {
                "id": "doi:10.1007/978-1-4020-9632-7 meta:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
            },
            {
                "id": "issn:0022-3727 meta:br/0604",
                "title": "Journal Of Physics D: Applied Physics",
                "author": "",
                "date": "",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "journal",
                "publisher": "",
                "editor": ""
            }
        ]
        format_expected = 'application/json'
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:x['date']), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:x['date'])
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_author(self):
        operation_url = 'author'
        request = '0000-0003-3891-6869'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 meta:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
                "date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266]",
                "editor": ""
            }]
        format_expected = 'application/json'
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_editor(self):
        operation_url = 'editor'
        request = '0000-0003-2098-4759'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 meta:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
            }]
        format_expected = 'application/json'
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_id(self):
        operation_url = 'search'
        request = 'id=doi:10.1007/978-1-4020-9632-7'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 isbn:9789048127108 isbn:9781402096327 meta:br/0601",
                "title": "Adaptive Environmental Management",
                "author": "",
                "date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
            }
        ]
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_title(self):
        operation_url = 'search'
        request = 'title=Adaptive Environmental Management'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 isbn:9789048127108 isbn:9781402096327 meta:br/0601",
                "title": "Adaptive Environmental Management",
                "author": "",
                "date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
            }
        ]
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_author(self):
        operation_url = 'search'
        request = 'author=Montijn,Carolynne'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 meta:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
                "date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266]",
                "editor": ""
            }
        ]
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_given_name(self):
        operation_url = 'search'
        request = 'author=,Carolynne'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 meta:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
                "date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266]",
                "editor": ""
            }
        ]
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_foaf_name(self):
        operation_url = 'search'
        request = 'author=F42'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1520/f2792-10e01 meta:br/0603",
                "title": "Terminology For Additive Manufacturing Technologies,",
                "author": "F42 Committee",
                "date": "",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "standard",
                "publisher": "Astm International [crossref:381]",
                "editor": ""
            }
        ]
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_editor(self):
        operation_url = 'search'
        request = 'editor=Stankey, George H.'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 isbn:9789048127108 isbn:9781402096327 meta:br/0601",
                "title": "Adaptive Environmental Management",
                "author": "",
                "date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
            }
        ]
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_publisher(self):
        operation_url = 'search'
        request = 'publisher=Springer Science And Business Media Llc'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 isbn:9789048127108 isbn:9781402096327 meta:br/0601",
                "title": "Adaptive Environmental Management",
                "author": "",
                "date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
            }
        ]
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_venue(self):
        operation_url = 'search'
        request = 'venue=Physics'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 meta:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
                "date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266]",
                "editor": ""
            }
        ]
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:''.join(x['id'])), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:''.join(x['id']))
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_volume_and_issue(self):
        operation_url = 'search'
        request = 'venue=Physics&&volume=39&&issue=14'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 meta:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
                "date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266]",
                "editor": ""
            }
        ]
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:''.join(x['id'])), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:''.join(x['id']))
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_volume_and_issue_error(self):
        operation_url = 'search'
        request = 'volume=39||issue=14'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, _, _ = op.exec()
        self.assertEqual(status, 500)

    def test_text_search_venue_and_author(self):
        operation_url = 'search'
        request = 'venue=Physics&&author=Montijn, Carolynne'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 meta:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
                "date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266]",
                "editor": ""
            }
        ]
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:''.join(x['id'])), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:''.join(x['id']))
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_author_or_editor(self):
        operation_url = 'search'
        request = 'editor=Allan, Catherine||author=Montijn, Carolynne'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 meta:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
                "date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266]",
                "editor": ""
            },
            {
                "id": "doi:10.1007/978-1-4020-9632-7 meta:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
            }
        ]
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:''.join(x['id'])), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:''.join(x['id']))
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_text_search_author_and_publisher_or_editor_and_title(self):
        operation_url = 'search'
        request = 'author=Montijn, Carolynne&&publisher=Iop Publishing||editor=Allan, Catherine&&title=Adaptive Environmental Management'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        format_expected = 'application/json'
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 meta:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
                "date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266]",
                "editor": ""
            },
            {
                "id": "doi:10.1007/978-1-4020-9632-7 meta:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
            }
        ]
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:''.join(x['id'])), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:''.join(x['id']))
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)







