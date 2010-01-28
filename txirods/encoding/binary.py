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
from string import Template
from construct import Enum, Struct, CString, UBInt32, UBInt64, MetaArray, IfThenElse
from construct import MappingAdapter, Pass, Select, Const, Field, Array

from txirods.genquery import const_to_int, int_to_const

NULL_PTR_PACK_STR = "%@#ANULLSTR$%\0"

header = Template("""<MsgHeader_PI>
<type>$type</type>
<msgLen>$msg_len</msgLen>
<errorLen>$err_len</errorLen>
<bsLen>$bs_len</bsLen>
<intInfo>$int_info</intInfo>
</MsgHeader_PI>\n""")

connect = Template("""<StartupPack_PI>
<irodsProt>$irodsProt</irodsProt>
<reconnFlag>$reconnFlag</reconnFlag>
<connectCnt>$connectCnt</connectCnt>
<proxyUser>$proxy_user</proxyUser>
<proxyRcatZone>$proxy_zone</proxyRcatZone>
<clientUser>$client_user</clientUser>
<clientRcatZone>$client_zone</clientRcatZone>
<relVersion>rods2.1</relVersion>
<apiVersion>d</apiVersion>
<option>$option</option>
</StartupPack_PI>\n""")
connect_default = {'irodsProt':0, 'reconnFlag': 0,
                   'connectCnt': 0, 'proxy_user': '',
                   'proxy_zone': '', 'client_user': '',
                   'client_zone': '', 'option': ''}

def count(context):
    return context.len

def nulls(context):
    if context.len == 0:
        return False
    return True


Null_Pointer = MappingAdapter(Const(Field('null', 14), NULL_PTR_PACK_STR), {NULL_PTR_PACK_STR: None}, {None: NULL_PTR_PACK_STR}, Pass, Pass)


keyValPair = Struct('keyValPair',
                    UBInt32('len'),
                    IfThenElse('keyWords', nulls, MetaArray(count, CString('key')), Null_Pointer),
                    IfThenElse('values', nulls, MetaArray(count, CString('value')), Null_Pointer)
                   )


Gen_Query_Mapper = MappingAdapter(UBInt32('const'), int_to_const, const_to_int)

inxIvalPair = Struct('inxIvalPair',
                     UBInt32('len'),
                     IfThenElse('inx', nulls, MetaArray(count, UBInt32('key')), Null_Pointer),
                     IfThenElse('value', nulls, MetaArray(count, UBInt32('value')), Null_Pointer)
                    )


inxValPair = Struct('inxValPair',
                     UBInt32('len'),
                     IfThenElse('inx', nulls, MetaArray(count, UBInt32('key')), Null_Pointer),
                     IfThenElse('value', nulls, MetaArray(count, CString('value')), Null_Pointer)
                    )


objType = Enum(UBInt32('objType'),
               UNKNOWN_OBJ_T = 0x00,
               DATA_OBJ_T = 0x01,
               COLL_OBJ_T = 0x02,
               UNKNOWN_FILE_T = 0x03,
               LOCAL_FILE_T = 0x04,
               LOCAL_DIR_T = 0x05,
               NO_INPUT_T = 0x06
              )



structFileType = Enum(UBInt32('structFileType'),
                      HAAW_STRUCT_FILE_T = 0x00,
                      TAR_STRUCT_FILE_T = 0x01
                     )


specCollClass = Enum(UBInt32('specCollClass'),
                     NO_SPEC_COLL = 0x00,
                     STRUCT_FILE_COLL = 0x01,
                     MOUNTED_COLL = 0x02
                    )


specColl = Struct('specColl',
                  specCollClass,
                  structFileType,
                  CString('collection'),
                  CString('objPath'),
                  CString('resource'),
                  CString('phyPath'),
                  CString('cacheDir'),
                  UBInt32('cacheDirty'),
                  UBInt32('replNum')
                 )


rodsObjStat = Struct('rodsObjStat_t',
                     UBInt64('objSize'),
                     objType,
                     UBInt32('dataMode'),
                     CString('dataId'),
                     CString('chksum'),
                     CString('ownerName'),
                     CString('ownerZone'),
                     CString('createTime'),
                     CString('modifyTime'),
                     Select('specColl',
                           Null_Pointer,
                           specColl
                          ),
                    )


genQueryInp = Struct('genQueryInp',
                     UBInt32('maxRows'),
                     UBInt32('continueInx'),
                     UBInt32('partialStartIndex'),
                     UBInt32('options'),
                     keyValPair,
                     inxIvalPair,
                     inxValPair,
                    )


dataObjInp = Struct('dataObjInp',
                    CString('objPath'),
                    UBInt32('createMode'),
                    UBInt32('openFlags'),
                    UBInt64('offset'),
                    UBInt64('dataSize'),
                    UBInt32('numThreads'),
                    UBInt32('oprType'),
                    Select('specColl',
                           Null_Pointer,
                           specColl
                          ),
                    keyValPair
                   )


sqlResult = Struct('sqlResult',
                   Gen_Query_Mapper,
                   UBInt32('len'),
                   Select('value',
                          Null_Pointer,
                          MetaArray(lambda c: c._.rowCnt, CString('value'))
                         ),
                  )


genQueryOut = Struct('genQueryOut',
                     UBInt32('rowCnt'),
                     UBInt32('attriCnt'),
                     UBInt32('continueInx'),
                     UBInt32('totalRowCount'),
                     MetaArray(lambda c: c.attriCnt, (sqlResult)),
                    )


