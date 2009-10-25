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


