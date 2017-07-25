# -*- coding: utf-8 -*-
import os

from app import create_app


class TestStatus:

    def setup(self):
        env = os.environ.get('APP_ENV', 'test')
        app = create_app('app.config.settings.%sConfig' % env.capitalize(), env=env)
        self.app = app.test_client()

    def teardown(self):
        pass

    def test_status(self):
        response = self.app.get(
            '/v1/status'
        )
        assert response.status_code == 200
