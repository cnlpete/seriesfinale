# -*- coding: utf-8 -*-

###########################################################################
#    SeriesFinale
#    Copyright (C) 2009 Joaquim Rocha <jrocha@igalia.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

import os
from SeriesFinale.lib import constants
from xml.etree import ElementTree as ET

class Settings(object):

    ASCENDING_ORDER = 0
    DESCENDING_ORDER = 1

    ALPHABETIC_ORDER = 0
    RECENT_EPISODE = 1
    LAST_AIRED_EPISODE = 2

    AUTOMATIC = 0
    PORTRAIT = 1
    LANDSCAPE = 2

    EPISODES_ORDER_CONF_NAME = 'episodes_order'
    SEASONS_ORDER_CONF_NAME = 'seasons_order'
    SHOWS_SORT = 'shows_sort'
    SHOWS_SORT_BY_GENRE = 'sort_by_genre'
    SHOWS_SORT_BY_PRIO = 'sort_by_prio'
    SCREEN_ROTATION = 'screen_rotation'
    ADD_SPECIAL_SEASONS = 'add_special_seasons'
    EPISODES_CHECK_POSITION = 'episodes_check_position'
    HIDE_COMPLETED_SHOWS = 'hide_completed_shows'
    SEARCH_LANGUAGE = 'search_language'
    UPDATE_ENDED_SHOWS = 'update_ended_shows'
    LAST_COMPLETE_UPDATE = 'last_complete_update'
    HIGHLIGHT_SPECIAL = 'highlight_special'

    LEFT = 0
    RIGHT = 1

    TYPES = {EPISODES_ORDER_CONF_NAME: int,
             SEASONS_ORDER_CONF_NAME: int,
             SHOWS_SORT: int,
             SHOWS_SORT_BY_GENRE: bool,
             SHOWS_SORT_BY_PRIO: bool,
             SCREEN_ROTATION: int,
             ADD_SPECIAL_SEASONS: bool,
             EPISODES_CHECK_POSITION: int,
             HIDE_COMPLETED_SHOWS: bool,
             SEARCH_LANGUAGE: str,
             UPDATE_ENDED_SHOWS: bool,
             LAST_COMPLETE_UPDATE: str,
             HIGHLIGHT_SPECIAL: bool}
    DEFAULTS = {EPISODES_ORDER_CONF_NAME: DESCENDING_ORDER,
                SEASONS_ORDER_CONF_NAME: ASCENDING_ORDER,
                SHOWS_SORT: RECENT_EPISODE,
                SHOWS_SORT_BY_GENRE: False,
                SHOWS_SORT_BY_PRIO: False,
                SCREEN_ROTATION: AUTOMATIC,
                ADD_SPECIAL_SEASONS: True,
                EPISODES_CHECK_POSITION: RIGHT,
                HIDE_COMPLETED_SHOWS: False,
                SEARCH_LANGUAGE: 'en',
                UPDATE_ENDED_SHOWS: True,
                LAST_COMPLETE_UPDATE: '-',
                HIGHLIGHT_SPECIAL: False}

    conf = dict(DEFAULTS)
    changed = False

    def load(self, conf_file):
        if not (os.path.exists(conf_file) and os.path.isfile(conf_file)):
            return

        tree = ET.ElementTree()
        tree.parse(conf_file)
        root = tree.getroot()
        for key in self.DEFAULTS.keys():
            key_element = root.find(key)
            if key_element is not None:
                if self.TYPES[key] == bool:
                    self.setConf(key, key_element.text.lower() == 'true')
                    continue
                self.setConf(key, self.TYPES[key](key_element.text))
        self.__class__.changed = False

    def save(self, conf_file):
        if not self.__class__.changed:
            return
        dirname = os.path.dirname(conf_file)
        if not (os.path.exists(dirname) and os.path.isdir(dirname)):
            os.mkdir(dirname)
        root = ET.Element(constants.SF_COMPACT_NAME)
        for key, value in self.__class__.conf.items():
            element = ET.SubElement(root, key)
            element.text = str(value)
        ET.ElementTree(root).write(conf_file, 'UTF-8')
        self.__class__.changed = False

    def setConf(self, key, value):
        if self.__class__.conf[key] != value:
            self.__class__.conf[key] = value
            self.__class__.changed = True

    def getConf(self, key):
        return self.TYPES[key](self.__class__.conf[key])
