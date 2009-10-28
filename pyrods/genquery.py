#############################################################################
#
# Copyright (c) 2009 Victorian Partnership for Advanced Computing Ltd and
# Contributors.
# All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

const_to_int = {}
int_to_const = {}


class Constant(int):
    def __new__(cls, name, value, **kwargs):
        inst = super(Constant, cls).__new__(cls, value, **kwargs)
        inst._name = name
        global const_to_int, int_to_const
        const_to_int[value] = inst
        int_to_const[value] = inst

        def new_tostr(self):
            return self._name.__str__()

        inst.__str__ = new_tostr
        return inst

Constant("EMPTY", 0)

# R_ZONE_MAIN:
COL_ZONE_ID = Constant('COL_ZONE_ID', 101)
COL_ZONE_NAME = Constant('COL_ZONE_NAME', 102)
COL_ZONE_TYPE = Constant('COL_ZONE_TYPE', 103)
COL_ZONE_CONNECTION = Constant('COL_ZONE_CONNECTION', 104)
COL_ZONE_COMMENT = Constant('COL_ZONE_COMMENT', 105)
COL_ZONE_CREATE_TIME = Constant('COL_ZONE_CREATE_TIME', 106)
COL_ZONE_MODIFY_TIME = Constant('COL_ZONE_MODIFY_TIME', 107)

# R_USER_MAIN:
COL_USER_ID = Constant('COL_USER_ID', 201)
COL_USER_NAME = Constant('COL_USER_NAME', 202)
COL_USER_TYPE = Constant('COL_USER_TYPE', 203)
COL_USER_ZONE = Constant('COL_USER_ZONE', 204)
COL_USER_DN = Constant('COL_USER_DN', 205)
COL_USER_INFO = Constant('COL_USER_INFO', 206)
COL_USER_COMMENT = Constant('COL_USER_COMMENT', 207)
COL_USER_CREATE_TIME = Constant('COL_USER_CREATE_TIME', 208)
COL_USER_MODIFY_TIME = Constant('COL_USER_MODIFY_TIME', 209)

# R_RESC_MAIN:
COL_R_RESC_ID = Constant('COL_R_RESC_ID', 301)
COL_R_RESC_NAME = Constant('COL_R_RESC_NAME', 302)
COL_R_ZONE_NAME = Constant('COL_R_ZONE_NAME', 303)
COL_R_TYPE_NAME = Constant('COL_R_TYPE_NAME', 304)
COL_R_CLASS_NAME = Constant('COL_R_CLASS_NAME', 305)
COL_R_LOC = Constant('COL_R_LOC', 306)
COL_R_VAULT_PATH = Constant('COL_R_VAULT_PATH', 307)
COL_R_FREE_SPACE = Constant('COL_R_FREE_SPACE', 308)
COL_R_RESC_INFO  = Constant('COL_R_RESC_INFO ', 309)
COL_R_RESC_COMMENT = Constant('COL_R_RESC_COMMENT', 310)
COL_R_CREATE_TIME = Constant('COL_R_CREATE_TIME', 311)
COL_R_MODIFY_TIME = Constant('COL_R_MODIFY_TIME', 312)
COL_R_RESC_STATUS = Constant('COL_R_RESC_STATUS', 313)
COL_R_FREE_SPACE_TIME = Constant('COL_R_FREE_SPACE_TIME', 314)

# R_DATA_MAIN:
COL_D_DATA_ID = Constant('COL_D_DATA_ID', 401)
COL_D_COLL_ID = Constant('COL_D_COLL_ID', 402)
COL_DATA_NAME = Constant('COL_DATA_NAME', 403)
COL_DATA_REPL_NUM = Constant('COL_DATA_REPL_NUM', 404)
COL_DATA_VERSION = Constant('COL_DATA_VERSION', 405)
COL_DATA_TYPE_NAME = Constant('COL_DATA_TYPE_NAME', 406)
COL_DATA_SIZE = Constant('COL_DATA_SIZE', 407)
COL_D_RESC_GROUP_NAME = Constant('COL_D_RESC_GROUP_NAME', 408)
COL_D_RESC_NAME = Constant('COL_D_RESC_NAME', 409)
COL_D_DATA_PATH = Constant('COL_D_DATA_PATH', 410)
COL_D_OWNER_NAME = Constant('COL_D_OWNER_NAME', 411)
COL_D_OWNER_ZONE = Constant('COL_D_OWNER_ZONE', 412)
COL_D_REPL_STATUS = Constant('COL_D_REPL_STATUS', 413) # isDirty
COL_D_DATA_STATUS = Constant('COL_D_DATA_STATUS', 414)
COL_D_DATA_CHECKSUM = Constant('COL_D_DATA_CHECKSUM', 415)
COL_D_EXPIRY = Constant('COL_D_EXPIRY', 416)
COL_D_MAP_ID = Constant('COL_D_MAP_ID', 417)
COL_D_COMMENTS = Constant('COL_D_COMMENTS', 418)
COL_D_CREATE_TIME = Constant('COL_D_CREATE_TIME', 419)
COL_D_MODIFY_TIME = Constant('COL_D_MODIFY_TIME', 420)
COL_DATA_MODE = Constant('COL_DATA_MODE', 421)

# R_COLL_MAIN
COL_COLL_ID = Constant('COL_COLL_ID', 500)
COL_COLL_NAME = Constant('COL_COLL_NAME', 501)
COL_COLL_PARENT_NAME = Constant('COL_COLL_PARENT_NAME', 502)
COL_COLL_OWNER_NAME = Constant('COL_COLL_OWNER_NAME', 503)
COL_COLL_OWNER_ZONE = Constant('COL_COLL_OWNER_ZONE', 504)
COL_COLL_MAP_ID = Constant('COL_COLL_MAP_ID', 505)
COL_COLL_INHERITANCE = Constant('COL_COLL_INHERITANCE', 506)
COL_COLL_COMMENTS = Constant('COL_COLL_COMMENTS', 507)
COL_COLL_CREATE_TIME = Constant('COL_COLL_CREATE_TIME', 508)
COL_COLL_MODIFY_TIME = Constant('COL_COLL_MODIFY_TIME', 509)
COL_COLL_TYPE = Constant('COL_COLL_TYPE', 510)
COL_COLL_INFO1 = Constant('COL_COLL_INFO1', 511)
COL_COLL_INFO2 = Constant('COL_COLL_INFO2', 512)

# R_META_MAIN
COL_META_DATA_ATTR_NAME = Constant('COL_META_DATA_ATTR_NAME', 600)
COL_META_DATA_ATTR_VALUE = Constant('COL_META_DATA_ATTR_VALUE', 601)
COL_META_DATA_ATTR_UNITS = Constant('COL_META_DATA_ATTR_UNITS', 602)
COL_META_DATA_ATTR_ID = Constant('COL_META_DATA_ATTR_ID', 603)
COL_META_DATA_CREATE_TIME = Constant('COL_META_DATA_CREATE_TIME', 604)
COL_META_DATA_MODIFY_TIME = Constant('COL_META_DATA_MODIFY_TIME', 605)

COL_META_COLL_ATTR_NAME = Constant('COL_META_COLL_ATTR_NAME', 610)
COL_META_COLL_ATTR_VALUE = Constant('COL_META_COLL_ATTR_VALUE', 611)
COL_META_COLL_ATTR_UNITS = Constant('COL_META_COLL_ATTR_UNITS', 612)
COL_META_COLL_ATTR_ID = Constant('COL_META_COLL_ATTR_ID', 613)

COL_META_NAMESPACE_COLL = Constant('COL_META_NAMESPACE_COLL', 620)
COL_META_NAMESPACE_DATA = Constant('COL_META_NAMESPACE_DATA', 621)
COL_META_NAMESPACE_RESC = Constant('COL_META_NAMESPACE_RESC', 622)
COL_META_NAMESPACE_USER = Constant('COL_META_NAMESPACE_USER', 623)

COL_META_RESC_ATTR_NAME = Constant('COL_META_RESC_ATTR_NAME', 630)
COL_META_RESC_ATTR_VALUE = Constant('COL_META_RESC_ATTR_VALUE', 631)
COL_META_RESC_ATTR_UNITS = Constant('COL_META_RESC_ATTR_UNITS', 632)
COL_META_RESC_ATTR_ID = Constant('COL_META_RESC_ATTR_ID', 633)

COL_META_USER_ATTR_NAME = Constant('COL_META_USER_ATTR_NAME', 640)
COL_META_USER_ATTR_VALUE = Constant('COL_META_USER_ATTR_VALUE', 641)
COL_META_USER_ATTR_UNITS = Constant('COL_META_USER_ATTR_UNITS', 642)
COL_META_USER_ATTR_ID = Constant('COL_META_USER_ATTR_ID', 643)

# R_OBJT_ACCESS
COL_DATA_ACCESS_TYPE = Constant('COL_DATA_ACCESS_TYPE', 700)
COL_DATA_ACCESS_NAME = Constant('COL_DATA_ACCESS_NAME', 701)
COL_DATA_TOKEN_NAMESPACE = Constant('COL_DATA_TOKEN_NAMESPACE', 702)
COL_DATA_ACCESS_USER_ID = Constant('COL_DATA_ACCESS_USER_ID', 703)
COL_DATA_ACCESS_DATA_ID = Constant('COL_DATA_ACCESS_DATA_ID', 704)

COL_COLL_ACCESS_TYPE = Constant('COL_COLL_ACCESS_TYPE', 710)
COL_COLL_ACCESS_NAME = Constant('COL_COLL_ACCESS_NAME', 711)
COL_COLL_TOKEN_NAMESPACE = Constant('COL_COLL_TOKEN_NAMESPACE', 712)
COL_COLL_ACCESS_USER_ID = Constant('COL_COLL_ACCESS_USER_ID', 713)
COL_COLL_ACCESS_COLL_ID = Constant('COL_COLL_ACCESS_COLL_ID', 714)

# R_RESC_GROUP
COL_RESC_GROUP_RESC_ID = Constant('COL_RESC_GROUP_RESC_ID', 800)
COL_RESC_GROUP_NAME = Constant('COL_RESC_GROUP_NAME', 801)

# R_USER_GROUP / USER
COL_USER_GROUP_ID = Constant('COL_USER_GROUP_ID', 900)
COL_USER_GROUP_NAME = Constant('COL_USER_GROUP_NAME', 901)

# R_RULE_EXEC
COL_RULE_EXEC_ID = Constant('COL_RULE_EXEC_ID', 1000)
COL_RULE_EXEC_NAME = Constant('COL_RULE_EXEC_NAME', 1001)
COL_RULE_EXEC_REI_FILE_PATH = Constant('COL_RULE_EXEC_REI_FILE_PATH', 1002)
COL_RULE_EXEC_USER_NAME   = Constant('COL_RULE_EXEC_USER_NAME  ', 1003)
COL_RULE_EXEC_ADDRESS = Constant('COL_RULE_EXEC_ADDRESS', 1004)
COL_RULE_EXEC_TIME    = Constant('COL_RULE_EXEC_TIME   ', 1005)
COL_RULE_EXEC_FREQUENCY = Constant('COL_RULE_EXEC_FREQUENCY', 1006)
COL_RULE_EXEC_PRIORITY = Constant('COL_RULE_EXEC_PRIORITY', 1007)
COL_RULE_EXEC_ESTIMATED_EXE_TIME = Constant('COL_RULE_EXEC_ESTIMATED_EXE_TIME', 1008)
COL_RULE_EXEC_NOTIFICATION_ADDR = Constant('COL_RULE_EXEC_NOTIFICATION_ADDR', 1009)
COL_RULE_EXEC_LAST_EXE_TIME = Constant('COL_RULE_EXEC_LAST_EXE_TIME', 1010)
COL_RULE_EXEC_STATUS = Constant('COL_RULE_EXEC_STATUS', 1011)

# R_TOKN_MAIN
COL_TOKEN_NAMESPACE = Constant('COL_TOKEN_NAMESPACE', 1100)
COL_TOKEN_ID = Constant('COL_TOKEN_ID', 1101)
COL_TOKEN_NAME = Constant('COL_TOKEN_NAME', 1102)
COL_TOKEN_VALUE = Constant('COL_TOKEN_VALUE', 1103)
COL_TOKEN_VALUE2 = Constant('COL_TOKEN_VALUE2', 1104)
COL_TOKEN_VALUE3 = Constant('COL_TOKEN_VALUE3', 1105)
COL_TOKEN_COMMENT = Constant('COL_TOKEN_COMMENT', 1106)

# R_OBJT_AUDIT
COL_AUDIT_OBJ_ID = Constant('COL_AUDIT_OBJ_ID', 1200)
COL_AUDIT_USER_ID = Constant('COL_AUDIT_USER_ID', 1201)
COL_AUDIT_ACTION_ID = Constant('COL_AUDIT_ACTION_ID', 1202)
COL_AUDIT_COMMENT = Constant('COL_AUDIT_COMMENT', 1203)
COL_AUDIT_CREATE_TIME = Constant('COL_AUDIT_CREATE_TIME', 1204)
COL_AUDIT_MODIFY_TIME = Constant('COL_AUDIT_MODIFY_TIME', 1205)

# Range of the Audit columns; used sometimes to restrict access
COL_AUDIT_RANGE_START = Constant('COL_AUDIT_RANGE_START', 1200)
COL_AUDIT_RANGE_END = Constant('COL_AUDIT_RANGE_END', 1299)

# R_COLL_USER_MAIN (r_user_main for Collection information)
COL_COLL_USER_NAME = Constant('COL_COLL_USER_NAME', 1300)
COL_COLL_USER_ZONE = Constant('COL_COLL_USER_ZONE', 1301)

# R_DATA_USER_MAIN (r_user_main for Data information specifically)
COL_DATA_USER_NAME = Constant('COL_DATA_USER_NAME', 1310)
COL_DATA_USER_ZONE = Constant('COL_DATA_USER_ZONE', 1311)

# R_SERVER_LOAD
COL_SL_HOST_NAME = Constant('COL_SL_HOST_NAME', 1400)
COL_SL_RESC_NAME = Constant('COL_SL_RESC_NAME', 1401)
COL_SL_CPU_USED = Constant('COL_SL_CPU_USED', 1402)
COL_SL_MEM_USED = Constant('COL_SL_MEM_USED', 1403)
COL_SL_SWAP_USED = Constant('COL_SL_SWAP_USED', 1404)
COL_SL_RUNQ_LOAD = Constant('COL_SL_RUNQ_LOAD', 1405)
COL_SL_DISK_SPACE = Constant('COL_SL_DISK_SPACE', 1406)
COL_SL_NET_INPUT = Constant('COL_SL_NET_INPUT', 1407)
COL_SL_NET_OUTPUT = Constant('COL_SL_NET_OUTPUT', 1408)
COL_SL_NET_OUTPUT = Constant('COL_SL_NET_OUTPUT', 1408)
COL_SL_CREATE_TIME = Constant('COL_SL_CREATE_TIME', 1409)

# R_SERVER_LOAD_DIGEST
COL_SLD_RESC_NAME = Constant('COL_SLD_RESC_NAME', 1500)
COL_SLD_LOAD_FACTOR = Constant('COL_SLD_LOAD_FACTOR', 1501)
COL_SLD_CREATE_TIME = Constant('COL_SLD_CREATE_TIME', 1502)

