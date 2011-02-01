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

int_to_cls = {}
const_to_cls = {}


class IRODSException(Exception):
    value = ""
    number = 0

    class __metaclass__(type):
        def __init__(cls, name, bases, dict):
            type.__init__(cls, name, bases, dict)
            if object not in bases:
                int_to_cls[cls.number] = cls
                const_to_cls[name] = cls

    def __str__(self):
        if self.value:
            return repr(str(self.number) + ': ' + self.value)
        return repr(str(self.number))


# 1,000 - 299,000 - system type
class SYS_SOCK_OPEN_ERR(IRODSException):
    number = -1000


class SYS_SOCK_BIND_ERR(IRODSException):
    number = -2000


class SYS_SOCK_ACCEPT_ERR(IRODSException):
    number = -3000


class SYS_HEADER_READ_LEN_ERR(IRODSException):
    number = -4000


class SYS_HEADER_WRITE_LEN_ERR(IRODSException):
    number = -5000


class SYS_HEADER_TPYE_LEN_ERR(IRODSException):
    number = -6000


class SYS_CAUGHT_SIGNAL(IRODSException):
    number = -7000


class SYS_GETSTARTUP_PACK_ERR(IRODSException):
    number = -8000


class SYS_EXCEED_CONNECT_CNT(IRODSException):
    number = -9000


class SYS_USER_NOT_ALLOWED_TO_CONN(IRODSException):
    number = -10000


class SYS_READ_MSG_BODY_INPUT_ERR(IRODSException):
    number = -11000


class SYS_UNMATCHED_API_NUM(IRODSException):
    number = -12000


class SYS_NO_API_PRIV(IRODSException):
    number = -13000


class SYS_API_INPUT_ERR(IRODSException):
    number = -14000


class SYS_PACK_INSTRUCT_FORMAT_ERR(IRODSException):
    number = -15000


class SYS_MALLOC_ERR(IRODSException):
    number = -16000


class SYS_GET_HOSTNAME_ERR(IRODSException):
    number = -17000


class SYS_OUT_OF_FILE_DESC(IRODSException):
    number = -18000


class SYS_FILE_DESC_OUT_OF_RANGE(IRODSException):
    number = -19000


class SYS_UNRECOGNIZED_REMOTE_FLAG(IRODSException):
    number = -20000


class SYS_INVALID_SERVER_HOST(IRODSException):
    number = -21000


class SYS_SVR_TO_SVR_CONNECT_FAILED(IRODSException):
    number = -22000


class SYS_BAD_FILE_DESCRIPTOR(IRODSException):
    number = -23000


class SYS_INTERNAL_NULL_INPUT_ERR(IRODSException):
    number = -24000


class SYS_CONFIG_FILE_ERR(IRODSException):
    number = -25000


class SYS_INVALID_ZONE_NAME(IRODSException):
    number = -26000


class SYS_COPY_LEN_ERR(IRODSException):
    number = -27000


class SYS_PORT_COOKIE_ERR(IRODSException):
    number = -28000


class SYS_KEY_VAL_TABLE_ERR(IRODSException):
    number = -29000


class SYS_INVALID_RESC_TYPE(IRODSException):
    number = -30000


class SYS_INVALID_FILE_PATH(IRODSException):
    number = -31000


class SYS_INVALID_RESC_INPUT(IRODSException):
    number = -32000


class SYS_INVALID_PORTAL_OPR(IRODSException):
    number = -33000


class SYS_PARA_OPR_NO_SUPPORT(IRODSException):
    number = -34000


class SYS_INVALID_OPR_TYPE(IRODSException):
    number = -35000


class SYS_NO_PATH_PERMISSION(IRODSException):
    number = -36000


class SYS_NO_ICAT_SERVER_ERR(IRODSException):
    number = -37000


class SYS_AGENT_INIT_ERR(IRODSException):
    number = -38000


class SYS_PROXYUSER_NO_PRIV(IRODSException):
    number = -39000


class SYS_NO_DATA_OBJ_PERMISSION(IRODSException):
    number = -40000


class SYS_DELETE_DISALLOWED(IRODSException):
    number = -41000


class SYS_OPEN_REI_FILE_ERR(IRODSException):
    number = -42000


class SYS_NO_RCAT_SERVER_ERR(IRODSException):
    number = -43000


class SYS_UNMATCH_PACK_INSTRUCTI_NAME(IRODSException):
    number = -44000


class SYS_SVR_TO_CLI_MSI_NO_EXIST(IRODSException):
    number = -45000


class SYS_COPY_ALREADY_IN_RESC(IRODSException):
    number = -46000


class SYS_RECONN_OPR_MISMATCH(IRODSException):
    number = -47000


class SYS_INPUT_PERM_OUT_OF_RANGE(IRODSException):
    number = -48000


class SYS_FORK_ERROR(IRODSException):
    number = -49000


class SYS_PIPE_ERROR(IRODSException):
    number = -50000


class SYS_EXEC_CMD_STATUS_SZ_ERROR(IRODSException):
    number = -51000


class SYS_PATH_IS_NOT_A_FILE(IRODSException):
    number = -52000


class SYS_UNMATCHED_SPEC_COLL_TYPE(IRODSException):
    number = -53000


class SYS_TOO_MANY_QUERY_RESULT(IRODSException):
    number = -54000


class SYS_SPEC_COLL_NOT_IN_CACHE(IRODSException):
    number = -55000


class SYS_SPEC_COLL_OBJ_NOT_EXIST(IRODSException):
    number = -56000


class SYS_REG_OBJ_IN_SPEC_COLL(IRODSException):
    number = -57000


class SYS_DEST_SPEC_COLL_SUB_EXIST(IRODSException):
    number = -58000


class SYS_SRC_DEST_SPEC_COLL_CONFLICT(IRODSException):
    number = -59000


class SYS_UNKNOWN_SPEC_COLL_CLASS(IRODSException):
    number = -60000


class SYS_DUPLICATE_XMSG_TICKET(IRODSException):
    number = -61000


class SYS_UNMATCHED_XMSG_TICKET(IRODSException):
    number = -62000


class SYS_NO_XMSG_FOR_MSG_NUMBER(IRODSException):
    number = -63000


class SYS_COLLINFO_2_FORMAT_ERR(IRODSException):
    number = -64000


class SYS_CACHE_STRUCT_FILE_RESC_ERR(IRODSException):
    number = -65000


class SYS_NOT_SUPPORTED(IRODSException):
    number = -66000


class SYS_TAR_STRUCT_FILE_EXTRACT_ERR(IRODSException):
    number = -67000


class SYS_STRUCT_FILE_DESC_ERR(IRODSException):
    number = -68000


class SYS_TAR_OPEN_ERR(IRODSException):
    number = -69000


class SYS_TAR_EXTRACT_ALL_ERR(IRODSException):
    number = -70000


class SYS_TAR_CLOSE_ERR(IRODSException):
    number = -71000


class SYS_STRUCT_FILE_PATH_ERR(IRODSException):
    number = -72000


class SYS_MOUNT_MOUNTED_COLL_ERR(IRODSException):
    number = -73000


class SYS_COLL_NOT_MOUNTED_ERR(IRODSException):
    number = -74000


class SYS_STRUCT_FILE_BUSY_ERR(IRODSException):
    number = -75000


class SYS_STRUCT_FILE_INMOUNTED_COLL(IRODSException):
    number = -76000


class SYS_COPY_NOT_EXIST_IN_RESC(IRODSException):
    number = -77000


class SYS_RESC_DOES_NOT_EXIST(IRODSException):
    number = -78000


class SYS_COLLECTION_NOT_EMPTY(IRODSException):
    number = -79000


class SYS_OBJ_TYPE_NOT_STRUCT_FILE(IRODSException):
    number = -80000


class SYS_WRONG_RESC_POLICY_FOR_BUN_OPR(IRODSException):
    number = -81000


class SYS_DIR_IN_VAULT_NOT_EMPTY(IRODSException):
    number = -82000


class SYS_OPR_FLAG_NOT_SUPPORT(IRODSException):
    number = -83000


class SYS_TAR_APPEND_ERR(IRODSException):
    number = -84000


class SYS_INVALID_PROTOCOL_TYPE(IRODSException):
    number = -85000


class SYS_UDP_CONNECT_ERR(IRODSException):
    number = -86000


class SYS_UDP_TRANSFER_ERR(IRODSException):
    number = -89000


class SYS_UDP_NO_SUPPORT_ERR(IRODSException):
    number = -90000


class SYS_READ_MSG_BODY_LEN_ERR(IRODSException):
    number = -91000


class CROSS_ZONE_SOCK_CONNECT_ERR(IRODSException):
    number = -92000


class SYS_NO_FREE_RE_THREAD(IRODSException):
    number = -93000


class SYS_BAD_RE_THREAD_INX(IRODSException):
    number = -94000


class SYS_CANT_DIRECTLY_ACC_COMPOUND_RESC(IRODSException):
    number = -95000


class SYS_SRC_DEST_RESC_COMPOUND_TYPE(IRODSException):
    number = -96000


class SYS_CACHE_RESC_NOT_ON_SAME_HOST(IRODSException):
    number = -97000


class SYS_NO_CACHE_RESC_IN_GRP(IRODSException):
    number = -98000


class SYS_UNMATCHED_RESC_IN_RESC_GRP(IRODSException):
    number = -99000


class SYS_CANT_MV_BUNDLE_DATA_TO_TRASH(IRODSException):
    number = -100000


class SYS_CANT_MV_BUNDLE_DATA_BY_COPY(IRODSException):
    number = -101000


class SYS_EXEC_TAR_ERR(IRODSException):
    number = -102000


class SYS_CANT_CHKSUM_COMP_RESC_DATA(IRODSException):
    number = -103000


class SYS_CANT_CHKSUM_BUNDLED_DATA(IRODSException):
    number = -104000


# 300,000 - 499,000 - user input type error
class USER_AUTH_SCHEME_ERR(IRODSException):
    number = -300000


class USER_AUTH_STRING_EMPTY(IRODSException):
    number = -301000


class USER_RODS_HOST_EMPTY(IRODSException):
    number = -302000


class USER_RODS_HOSTNAME_ERR(IRODSException):
    number = -303000


class USER_SOCK_OPEN_ERR(IRODSException):
    number = -304000


class USER_SOCK_CONNECT_ERR(IRODSException):
    number = -305000


class USER_STRLEN_TOOLONG(IRODSException):
    number = -306000


class USER_API_INPUT_ERR(IRODSException):
    number = -307000


class USER_PACKSTRUCT_INPUT_ERR(IRODSException):
    number = -308000


class USER_NO_SUPPORT_ERR(IRODSException):
    number = -309000


class USER_FILE_DOES_NOT_EXIST(IRODSException):
    number = -310000


class USER_FILE_TOO_LARGE(IRODSException):
    number = -311000


class OVERWITE_WITHOUT_FORCE_FLAG(IRODSException):
    number = -312000


class UNMATCHED_KEY_OR_INDEX(IRODSException):
    number = -313000


class USER_CHKSUM_MISMATCH(IRODSException):
    number = -314000


class USER_BAD_KEYWORD_ERR(IRODSException):
    number = -315000


class USER__NULL_INPUT_ERR(IRODSException):
    number = -316000


class USER_INPUT_PATH_ERR(IRODSException):
    number = -317000


class USER_INPUT_OPTION_ERR(IRODSException):
    number = -318000


class USER_INVALID_USERNAME_FORMAT(IRODSException):
    number = -319000


class USER_DIRECT_RESC_INPUT_ERR(IRODSException):
    number = -320000


class USER_NO_RESC_INPUT_ERR(IRODSException):
    number = -321000


class USER_PARAM_LABEL_ERR(IRODSException):
    number = -322000


class USER_PARAM_TYPE_ERR(IRODSException):
    number = -323000


class BASE64_BUFFER_OVERFLOW(IRODSException):
    number = -324000


class BASE64_INVALID_PACKET(IRODSException):
    number = -325000


class USER_MSG_TYPE_NO_SUPPORT(IRODSException):
    number = -326000


class USER_RSYNC_NO_MODE_INPUT_ERR(IRODSException):
    number = -337000


class USER_OPTION_INPUT_ERR(IRODSException):
    number = -338000


class SAME_SRC_DEST_PATHS_ERR(IRODSException):
    number = -339000


class USER_RESTART_FILE_INPUT_ERR(IRODSException):
    number = -340000


class RESTART_OPR_FAILED(IRODSException):
    number = -341000


class BAD_EXEC_CMD_PATH(IRODSException):
    number = -342000


class EXEC_CMD_OUTPUT_TOO_LARGE(IRODSException):
    number = -343000


class EXEC_CMD_ERROR(IRODSException):
    number = -344000


class BAD_INPUT_DESC_INDEX(IRODSException):
    number = -345000


class USER_PATH_EXCEEDS_MAX(IRODSException):
    number = -346000


class USER_SOCK_CONNECT_TIMEDOUT(IRODSException):
    number = -347000


class USER_API_VERSION_MISMATCH(IRODSException):
    number = -348000


class USER_INPUT_FORMAT_ERR(IRODSException):
    number = -349000


class USER_ACCESS_DENIED(IRODSException):
    number = -350000


class CANT_RM_MV_BUNDLE_TYPE(IRODSException):
    number = -351000


class NO_MORE_RESULT(IRODSException):
    number = -352000


class NO_KEY_WD_IN_MS_INP_STR(IRODSException):
    number = -353000


class CANT_RM_NON_EMPTY_HOME_COLL(IRODSException):
    number = -354000


class CANT_UNREG_IN_VAULT_FILE(IRODSException):
    number = -355000


# 500,000 to 800,000 - file driver error
class FILE_INDEX_LOOKUP_ERR(IRODSException):
    number = -500000


class UNIX_FILE_OPEN_ERR(IRODSException):
    number = -510000


class UNIX_FILE_CREATE_ERR(IRODSException):
    number = -511000


class UNIX_FILE_READ_ERR(IRODSException):
    number = -512000


class UNIX_FILE_WRITE_ERR(IRODSException):
    number = -513000


class UNIX_FILE_CLOSE_ERR(IRODSException):
    number = -514000


class UNIX_FILE_UNLINK_ERR(IRODSException):
    number = -515000


class UNIX_FILE_STAT_ERR(IRODSException):
    number = -516000


class UNIX_FILE_FSTAT_ERR(IRODSException):
    number = -517000


class UNIX_FILE_LSEEK_ERR(IRODSException):
    number = -518000


class UNIX_FILE_FSYNC_ERR(IRODSException):
    number = -519000


class UNIX_FILE_MKDIR_ERR(IRODSException):
    number = -520000


class UNIX_FILE_RMDIR_ERR(IRODSException):
    number = -521000


class UNIX_FILE_OPENDIR_ERR(IRODSException):
    number = -522000


class UNIX_FILE_CLOSEDIR_ERR(IRODSException):
    number = -523000


class UNIX_FILE_READDIR_ERR(IRODSException):
    number = -524000


class UNIX_FILE_STAGE_ERR(IRODSException):
    number = -525000


class UNIX_FILE_GET_FS_FREESPACE_ERR(IRODSException):
    number = -526000


class UNIX_FILE_CHMOD_ERR(IRODSException):
    number = -527000


class UNIX_FILE_RENAME_ERR(IRODSException):
    number = -528000


class UNIX_FILE_TRUNCATE_ERR(IRODSException):
    number = -529000


class UNIX_FILE_LINK_ERR(IRODSException):
    number = -530000


# 800,000 to 880,000 - Catalog library errors
class CATALOG_NOT_CONNECTED(IRODSException):
    number = -801000


class CAT_ENV_ERR(IRODSException):
    number = -802000


class CAT_CONNECT_ERR(IRODSException):
    number = -803000


class CAT_DISCONNECT_ERR(IRODSException):
    number = -804000


class CAT_CLOSE_ENV_ERR(IRODSException):
    number = -805000


class CAT_SQL_ERR(IRODSException):
    number = -806000


class CAT_GET_ROW_ERR(IRODSException):
    number = -807000


class CAT_NO_ROWS_FOUND(IRODSException):
    number = -808000


class CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME(IRODSException):
    number = -809000


class CAT_INVALID_RESOURCE_TYPE(IRODSException):
    number = -810000


class CAT_INVALID_RESOURCE_CLASS(IRODSException):
    number = -811000


class CAT_INVALID_RESOURCE_NET_ADDR(IRODSException):
    number = -812000


class CAT_INVALID_RESOURCE_VAULT_PATH(IRODSException):
    number = -813000


class CAT_UNKNOWN_COLLECTION(IRODSException):
    number = -814000


class CAT_INVALID_DATA_TYPE(IRODSException):
    number = -815000


class CAT_INVALID_ARGUMENT(IRODSException):
    number = -816000


class CAT_UNKNOWN_FILE(IRODSException):
    number = -817000


class CAT_NO_ACCESS_PERMISSION(IRODSException):
    number = -818000


class CAT_SUCCESS_BUT_WITH_NO_INFO(IRODSException):
    number = -819000


class CAT_INVALID_USER_TYPE(IRODSException):
    number = -820000


class CAT_COLLECTION_NOT_EMPTY(IRODSException):
    number = -821000


class CAT_TOO_MANY_TABLES(IRODSException):
    number = -822000


class CAT_UNKNOWN_TABLE(IRODSException):
    number = -823000


class CAT_NOT_OPEN(IRODSException):
    number = -824000


class CAT_FAILED_TO_LINK_TABLES(IRODSException):
    number = -825000


class CAT_INVALID_AUTHENTICATION(IRODSException):
    number = -826000


class CAT_INVALID_USER(IRODSException):
    number = -827000


class CAT_INVALID_ZONE(IRODSException):
    number = -828000


class CAT_INVALID_GROUP(IRODSException):
    number = -829000


class CAT_INSUFFICIENT_PRIVILEGE_LEVEL(IRODSException):
    number = -830000


class CAT_INVALID_RESOURCE(IRODSException):
    number = -831000


class CAT_INVALID_CLIENT_USER(IRODSException):
    number = -832000


class CAT_NAME_EXISTS_AS_COLLECTION(IRODSException):
    number = -833000


class CAT_NAME_EXISTS_AS_DATAOBJ(IRODSException):
    number = -834000


class CAT_RESOURCE_NOT_EMPTY(IRODSException):
    number = -835000


class CAT_NOT_A_DATAOBJ_AND_NOT_A_COLLECTION(IRODSException):
    number = -836000


class CAT_RECURSIVE_MOVE(IRODSException):
    number = -837000


class CAT_LAST_REPLICA(IRODSException):
    number = -838000


class CAT_OCI_ERROR(IRODSException):
    number = -839000


class CAT_PASSWORD_EXPIRED(IRODSException):
    number = -840000


class CAT_PASSWORD_ENCODING_ERROR(IRODSException):
    number = -850000


# 880,000 to 900,000  RDA errors
class RDA_NOT_COMPILED_IN(IRODSException):
    number = -880000


class RDA_NOT_CONNECTED(IRODSException):
    number = -881000


class RDA_ENV_ERR(IRODSException):
    number = -882000


class RDA_CONNECT_ERR(IRODSException):
    number = -883000


class RDA_DISCONNECT_ERR(IRODSException):
    number = -884000


class RDA_CLOSE_ENV_ERR(IRODSException):
    number = -885000


class RDA_SQL_ERR(IRODSException):
    number = -886000


class RDA_CONFIG_FILE_ERR(IRODSException):
    number = -887000


class RDA_ACCESS_PROHIBITED(IRODSException):
    number = -888000


class RDA_NAME_NOT_FOUND(IRODSException):
    number = -889000


# 900,000 to 920,000 - Misc errors (used by obf library, etc)
class FILE_OPEN_ERR(IRODSException):
    number = -900000


class FILE_READ_ERR(IRODSException):
    number = -901000


class FILE_WRITE_ERR(IRODSException):
    number = -902000


class PASSWORD_EXCEEDS_MAX_SIZE(IRODSException):
    number = -903000


class ENVIRONMENT_VAR_HOME_NOT_DEFINED(IRODSException):
    number = -904000


class UNABLE_TO_STAT_FILE(IRODSException):
    number = -905000


class AUTH_FILE_NOT_ENCRYPTED(IRODSException):
    number = -906000


class AUTH_FILE_DOES_NOT_EXIST(IRODSException):
    number = -907000


class UNLINK_FAILED(IRODSException):
    number = -908000


class NO_PASSWORD_ENTERED(IRODSException):
    number = -909000


class REMOTE_SERVER_AUTHENTICATION_FAILURE(IRODSException):
    number = -910000


class REMOTE_SERVER_AUTH_NOT_PROVIDED(IRODSException):
    number = -911000


class REMOTE_SERVER_AUTH_EMPTY(IRODSException):
    number = -912000


class REMOTE_SERVER_SID_NOT_DEFINED(IRODSException):
    number = -913000


# 921,000 to 999,000 - GSI and KRB errors
class GSI_NOT_COMPILED_IN(IRODSException):
    number = -921000


class GSI_NOT_BUILT_INTO_CLIENT(IRODSException):
    number = -922000


class GSI_NOT_BUILT_INTO_SERVER(IRODSException):
    number = -923000


class GSI_ERROR_IMPORT_NAME(IRODSException):
    number = -924000


class GSI_ERROR_INIT_SECURITY_CONTEXT(IRODSException):
    number = -925000


class GSI_ERROR_SENDING_TOKEN_LENGTH(IRODSException):
    number = -926000


class GSI_ERROR_READING_TOKEN_LENGTH(IRODSException):
    number = -927000


class GSI_ERROR_TOKEN_TOO_LARGE(IRODSException):
    number = -928000


class GSI_ERROR_BAD_TOKEN_RCVED(IRODSException):
    number = -929000


class GSI_SOCKET_READ_ERROR(IRODSException):
    number = -930000


class GSI_PARTIAL_TOKEN_READ(IRODSException):
    number = -931000


class GSI_SOCKET_WRITE_ERROR(IRODSException):
    number = -932000


class GSI_ERROR_FROM_GSI_LIBRARY(IRODSException):
    number = -933000


class GSI_ERROR_IMPORTING_NAME(IRODSException):
    number = -934000


class GSI_ERROR_ACQUIRING_CREDS(IRODSException):
    number = -935000


class GSI_ACCEPT_SEC_CONTEXT_ERROR(IRODSException):
    number = -936000


class GSI_ERROR_DISPLAYING_NAME(IRODSException):
    number = -937000


class GSI_ERROR_RELEASING_NAME(IRODSException):
    number = -938000


class GSI_DN_DOES_NOT_MATCH_USER(IRODSException):
    number = -939000


class GSI_QUERY_INTERNAL_ERROR(IRODSException):
    number = -940000


class KRB_NOT_COMPILED_IN(IRODSException):
    number = -951000


class KRB_NOT_BUILT_INTO_CLIENT(IRODSException):
    number = -952000


class KRB_NOT_BUILT_INTO_SERVER(IRODSException):
    number = -953000


class KRB_ERROR_IMPORT_NAME(IRODSException):
    number = -954000


class KRB_ERROR_INIT_SECURITY_CONTEXT(IRODSException):
    number = -955000


class KRB_ERROR_SENDING_TOKEN_LENGTH(IRODSException):
    number = -956000


class KRB_ERROR_READING_TOKEN_LENGTH(IRODSException):
    number = -957000


class KRB_ERROR_TOKEN_TOO_LARGE(IRODSException):
    number = -958000


class KRB_ERROR_BAD_TOKEN_RCVED(IRODSException):
    number = -959000


class KRB_SOCKET_READ_ERROR(IRODSException):
    number = -960000


class KRB_PARTIAL_TOKEN_READ(IRODSException):
    number = -961000


class KRB_SOCKET_WRITE_ERROR(IRODSException):
    number = -962000


class KRB_ERROR_FROM_KRB_LIBRARY(IRODSException):
    number = -963000


class KRB_ERROR_IMPORTING_NAME(IRODSException):
    number = -964000


class KRB_ERROR_ACQUIRING_CREDS(IRODSException):
    number = -965000


class KRB_ACCEPT_SEC_CONTEXT_ERROR(IRODSException):
    number = -966000


class KRB_ERROR_DISPLAYING_NAME(IRODSException):
    number = -967000


class KRB_ERROR_RELEASING_NAME(IRODSException):
    number = -968000


class KRB_USER_DN_NOT_FOUND(IRODSException):
    number = -969000


class KRB_NAME_MATCHES_MULTIPLE_USERS(IRODSException):
    number = -970000


class KRB_QUERY_INTERNAL_ERROR(IRODSException):
    number = -971000


# 1,000,000 to 1,500,000  - Rule Engine errors
class OBJPATH_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1000000


class RESCNAME_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1001000


class DATATYPE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1002000


class DATASIZE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1003000


class CHKSUM_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1004000


class VERSION_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1005000


class FILEPATH_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1006000


class REPLNUM_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1007000


class REPLSTATUS_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1008000


class DATAOWNER_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1009000


class DATAOWNERZONE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1010000


class DATAEXPIRY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1011000


class DATACOMMENTS_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1012000


class DATACREATE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1013000


class DATAMODIFY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1014000


class DATAACCESS_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1015000


class DATAACCESSINX_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1016000


class NO_RULE_FOUND_ERR(IRODSException):
    number = -1017000


class NO_MORE_RULES_ERR(IRODSException):
    number = -1018000


class UNMATCHED_ACTION_ERR(IRODSException):
    number = -1019000


class RULES_FILE_READ_ERROR(IRODSException):
    number = -1020000


class ACTION_ARG_COUNT_MISMATCH(IRODSException):
    number = -1021000


class MAX_NUM_OF_ARGS_IN_ACTION_EXCEEDED(IRODSException):
    number = -1022000


class UNKNOWN_PARAM_IN_RULE_ERR(IRODSException):
    number = -1023000


class DESTRESCNAME_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1024000


class BACKUPRESCNAME_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1025000


class DATAID_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1026000


class COLLID_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1027000


class RESCGROUPNAME_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1028000


class STATUSSTRING_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1029000


class DATAMAPID_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1030000


class USERNAMECLIENT_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1031000


class RODSZONECLIENT_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1032000


class USERTYPECLIENT_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1033000


class HOSTCLIENT_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1034000


class AUTHSTRCLIENT_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1035000


class USERAUTHSCHEMECLIENT_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1036000


class USERINFOCLIENT_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1037000


class USERCOMMENTCLIENT_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1038000


class USERCREATECLIENT_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1039000


class USERMODIFYCLIENT_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1040000


class USERNAMEPROXY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1041000


class RODSZONEPROXY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1042000


class USERTYPEPROXY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1043000


class HOSTPROXY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1044000


class AUTHSTRPROXY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1045000


class USERAUTHSCHEMEPROXY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1046000


class USERINFOPROXY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1047000


class USERCOMMENTPROXY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1048000


class USERCREATEPROXY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1049000


class USERMODIFYPROXY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1050000


class COLLNAME_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1051000


class COLLPARENTNAME_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1052000


class COLLOWNERNAME_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1053000


class COLLOWNERZONE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1054000


class COLLEXPIRY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1055000


class COLLCOMMENTS_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1056000


class COLLCREATE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1057000


class COLLMODIFY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1058000


class COLLACCESS_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1059000


class COLLACCESSINX_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1060000


class COLLMAPID_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1062000


class COLLINHERITANCE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1063000


class RESCZONE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1065000


class RESCLOC_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1066000


class RESCTYPE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1067000


class RESCTYPEINX_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1068000


class RESCCLASS_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1069000


class RESCCLASSINX_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1070000


class RESCVAULTPATH_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1071000


class NUMOPEN_ORTS_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1072000


class PARAOPR_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1073000


class RESCID_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1074000


class GATEWAYADDR_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1075000


class RESCMAX_BJSIZE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1076000


class FREESPACE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1077000


class FREESPACETIME_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1078000


class FREESPACETIMESTAMP_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1079000


class RESCINFO_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1080000


class RESCCOMMENTS_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1081000


class RESCCREATE_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1082000


class RESCMODIFY_EMPTY_IN_STRUCT_ERR(IRODSException):
    number = -1083000


class INPUT_ARG_NOT_WELL_FORMED_ERR(IRODSException):
    number = -1084000


class INPUT_ARG_OUT_OF_ARGC_RANGE_ERR(IRODSException):
    number = -1085000


class INSUFFICIENT_INPUT_ARG_ERR(IRODSException):
    number = -1086000


class INPUT_ARG_DOES_NOT_MATCH_ERR(IRODSException):
    number = -1087000


class RETRY_WITHOUT_RECOVERY_ERR(IRODSException):
    number = -1088000


class CUT_ACTION_PROCESSED_ERR(IRODSException):
    number = -1089000


class ACTION_FAILED_ERR(IRODSException):
    number = -1090000


class FAIL_ACTION_ENCOUNTERED_ERR(IRODSException):
    number = -1091000


class VARIABLE_NAME_TOO_LONG_ERR(IRODSException):
    number = -1092000


class UNKNOWN_VARIABLE_MAP_ERR(IRODSException):
    number = -1093000


class UNDEFINED_VARIABLE_MAP_ERR(IRODSException):
    number = -1094000


class NULL_VALUE_ERR(IRODSException):
    number = -1095000


class DVARMAP_FILE_READ_ERROR(IRODSException):
    number = -1096000


class NO_RULE_OR_MSI_FUNCTION_FOUND_ERR(IRODSException):
    number = -1097000


class FILE_CREATE_ERROR(IRODSException):
    number = -1098000


class FMAP_FILE_READ_ERROR(IRODSException):
    number = -1099000


class DATE_FORMAT_ERR(IRODSException):
    number = -1100000


class RULE_FAILED_ERR(IRODSException):
    number = -1101000


class NO_MICROSERVICE_FOUND_ERR(IRODSException):
    number = -1102000


class INVALID_REGEXP(IRODSException):
    number = -1103000


class INVALID_OBJECT_NAME(IRODSException):
    number = -1104000


class INVALID_OBJECT_TYPE(IRODSException):
    number = -1105000


class NO_VALUES_FOUND(IRODSException):
    number = -1106000


class NO_COLUMN_NAME_FOUND(IRODSException):
    number = -1107000


class BREAK_ACTION_ENCOUNTERED_ERR(IRODSException):
    number = -1108000


class CUT_ACTION_ON_SUCCESS_PROCESSED_ERR(IRODSException):
    number = -1109000


# 1,600,000 to 1,700,000  - PHP scripting error
class PHP_EXEC_SCRIPT_ERR(IRODSException):
    number = -1600000


class PHP_REQUEST_STARTUP_ERR(IRODSException):
    number = -1601000


class PHP_OPEN_SCRIPT_FILE_ERR(IRODSException):
    number = -1602000


# The following are handler protocol type msg. These are not real error
class SYS_NULL_INPUT(IRODSException):
    number = -99999996


class SYS_HANDLER_DONE_WITH_ERROR(IRODSException):
    number = -99999997


class SYS_HANDLER_DONE_NO_ERROR(IRODSException):
    number = -99999998


class SYS_NO_HANDLER_REPLY_MSG(IRODSException):
    number = -99999999
