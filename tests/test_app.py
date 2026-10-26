import os, tempfile, unittest
import app as app_module
import database
class AppTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.NamedTemporaryFile(delete=False); self.tmp.close(); app_module.DB=self.tmp.name; database.init_db(app_module.DB); app_module.app.config['TESTING']=True; self.client=app_module.app.test_client()
    def tearDown(self):
        try: os.unlink(self.tmp.name)
        except OSError: pass
    def test_health(self): self.assertEqual(self.client.get('/health').status_code,200)
    def test_create_and_visit_consent_declined(self):
        self.client.post('/links',data={'destination':'https://example.com','campaign':'test'},follow_redirects=True); rows=database.dashboard_rows(app_module.DB); self.assertEqual(len(rows),1); link_id=rows[0]['id']; self.assertEqual(self.client.get(f'/l/{link_id}').status_code,200); self.client.post(f'/l/{link_id}/continue',data={}); rows=database.dashboard_rows(app_module.DB); self.assertEqual(rows[0]['total_clicks'],1); self.assertEqual(rows[0]['consented_clicks'] or 0,0)
    def test_invalid_destination(self):
        self.client.post('/links',data={'destination':'javascript:alert(1)'},follow_redirects=True); self.assertEqual(database.dashboard_rows(app_module.DB),[])
if __name__=='__main__': unittest.main()
