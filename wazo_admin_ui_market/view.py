# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask import render_template
from flask import request
from flask import jsonify
from flask_menu.classy import classy_menu_item
from flask_classful import route

from wazo_admin_ui.helpers.classful import BaseView

from .market import get_market


class PluginView(BaseView):

    @classy_menu_item('.plugins', 'Plugins', order=0, icon="cubes")
    def index(self):
        return render_template('plugin/list.html')

    def list_plugin(self):
        market = get_market()
        plugins_installed = self.service.list()['items']
        for available_plugin in market['items']:
            for plugin_installed in plugins_installed:
                if available_plugin.get('namespace') == plugin_installed.get('namespace') and available_plugin.get('name') == plugin_installed.get('name'):
                    available_plugin['is_installed'] = True
                else:
                    available_plugin['is_installed'] = False

        return render_template('plugin/list_plugins.html', market=market['items'])

    @route('/install_plugin/', methods=['POST'])
    def install_plugin(self):
        body = request.get_json()
        plugin = self.service.install_plugin(body)
        return jsonify(plugin)

    @route('/remove_plugin/', methods=['POST'])
    def remove_plugin(self):
        body = request.get_json()
        self.service.uninstall_plugin(body)
        return jsonify(body)

    @route('/search_plugin/', methods=['POST'])
    def search_plugin(self):
        body = request.get_json()
        search = body['value']
        market = get_market()

        res = []
        for entry in market['items']:
            if search in entry.values():
                res.append(entry)

        return render_template('plugin/list_plugins.html', market=res)

    @route('/filter_plugin/', methods=['POST'])
    def filter_plugin(self):
        body = request.get_json()
        filter = body['value']
        market = get_market()
        plugins_installed = self.service.list()['items']
        for available_plugin in market['items']:
            for plugin_installed in plugins_installed:
                if available_plugin.get('namespace') == plugin_installed.get('namespace') and available_plugin.get('name') == plugin_installed.get('name'):
                    available_plugin['is_installed'] = True
                else:
                    available_plugin['is_installed'] = False

        if filter == 'installed':
            is_installed = True
        if filter == 'not_installed':
            is_installed = False
        if filter == 'all':
            return render_template('plugin/list_plugins.html', market=market['items'])

        results = []
        if is_installed:
            results = plugins_installed
            for result in results:
                result['is_installed'] = True
        else:
            for plugin in market['items']:
                if not plugin['is_installed']:
                    results.append(plugin)

        return render_template('plugin/list_plugins.html', market=results)
