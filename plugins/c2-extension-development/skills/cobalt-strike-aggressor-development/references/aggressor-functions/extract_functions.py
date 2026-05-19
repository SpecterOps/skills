#!/usr/bin/env python3
"""
Extract individual Aggressor function documentation from HTML file
and create separate markdown files for each function.
"""

import re
import os
from html.parser import HTMLParser
from pathlib import Path

# Function list with line ranges
FUNCTIONS = [
    ("-hasbootstraphint", 1183, 1192),
    ("-is64", 1193, 1206),
    ("-isactive", 1207, 1221),
    ("-isadmin", 1222, 1235),
    ("-isbeacon", 1236, 1249),
    ("-isssh", 1250, 1263),
    ("action", 1264, 1271),
    ("addTab", 1272, 1282),
    ("addVisualization", 1283, 1295),
    ("add_to_clipboard", 1296, 1303),
    ("alias", 1304, 1317),
    ("alias_clear", 1318, 1325),
    ("all_payloads", 1326, 1344),
    ("applications", 1345, 1352),
    ("archives", 1353, 1362),
    ("artifact", 1363, 1425),
    ("artifact_general", 1426, 1470),
    ("artifact_payload", 1471, 1531),
    ("artifact_sign", 1532, 1558),
    ("artifact_stageless", 1559, 1628),
    ("artifact_stager", 1629, 1688),
    ("barch", 1689, 1698),
    ("bargue_add", 1699, 1718),
    ("bargue_list", 1719, 1726),
    ("bargue_remove", 1727, 1736),
    ("base64_decode", 1737, 1746),
    ("base64_encode", 1747, 1756),
    ("bbeacon_config", 1757, 1863),
    ("bbeacon_gate", 1864, 1872),
    ("bblockdlls", 1873, 1886),
    ("bbrowser", 1887, 1897),
    ("bbrowserpivot", 1898, 1907),
    ("bbrowserpivot_stop", 1908, 1915),
    ("bbypassuac", 1916, 1921),
    ("bcancel", 1922, 1932),
    ("bcd", 1933, 1945),
    ("bcheckin", 1946, 1956),
    ("bclear", 1957, 1964),
    ("bclipboard", 1965, 1972),
    ("bconnect", 1973, 1984),
    ("bcovertvpn", 1985, 1995),
    ("bcp", 1996, 2005),
    ("bdata", 2006, 2015),
    ("bdata_store_list", 2016, 2023),
    ("bdata_store_load", 2024, 2034),
    ("bdata_store_unload", 2035, 2043),
    ("bdcsync", 2044, 2063),
    ("bdesktop", 2064, 2073),
    ("bdllinject", 2074, 2083),
    ("bdllload", 2084, 2095),
    ("bdllspawn", 2096, 2152),
    ("bdownload", 2153, 2161),
    ("bdrives", 2162, 2172),
    ("beacon_command_describe", 2173, 2182),
    ("beacon_command_detail", 2183, 2194),
    ("beacon_command_group", 2195, 2224),
    ("beacon_command_register", 2225, 2252),
    ("beacon_commands", 2253, 2260),
    ("beacon_data", 2261, 2270),
    ("beacon_elevator_describe", 2271, 2282),
    ("beacon_elevator_register", 2283, 2317),
    ("beacon_elevators", 2318, 2327),
    ("beacon_execute_job", 2328, 2348),
    ("beacon_execute_postex_job", 2349, 2367),
    ("beacon_exploit_describe", 2368, 2379),
    ("beacon_exploit_register", 2380, 2416),
    ("beacon_exploits", 2417, 2426),
    ("beacon_host_imported_script", 2427, 2454),
    ("beacon_host_script", 2455, 2472),
    ("beacon_ids", 2473, 2482),
    ("beacon_info", 2483, 2494),
    ("beacon_inline_execute", 2495, 2552),
    ("beacon_job_hide_output", 2553, 2563),
    ("beacon_job_name", 2564, 2572),
    ("beacon_link", 2573, 2585),
    ("beacon_remote_exec_method_describe", 2586, 2597),
    ("beacon_remote_exec_method_register", 2598, 2608),
    ("beacon_remote_exec_methods", 2609, 2618),
    ("beacon_remote_exploit_arch", 2619, 2630),
    ("beacon_remote_exploit_describe", 2631, 2642),
    ("beacon_remote_exploit_register", 2643, 2654),
    ("beacon_remote_exploits", 2655, 2664),
    ("beacon_remove", 2665, 2671),
    ("beacon_stage_pipe", 2672, 2691),
    ("beacon_stage_tcp", 2692, 2712),
    ("beacons", 2713, 2722),
    ("belevate", 2723, 2739),
    ("belevate_command", 2740, 2754),
    ("berror", 2755, 2765),
    ("bexecute", 2766, 2774),
    ("bexecute_assembly", 2775, 2799),
    ("bexit", 2800, 2810),
    ("bgetprivs", 2811, 2823),
    ("bgetsystem", 2824, 2834),
    ("bgetuid", 2835, 2841),
    ("bhashdump", 2842, 2857),
    ("bind", 2858, 2877),
    ("binfo", 2878, 2889),
    ("binject", 2890, 2900),
    ("binline_execute", 2901, 2913),
    ("binput", 2914, 2923),
    ("bipconfig", 2924, 2936),
    ("bjoberror", 2937, 2957),
    ("bjobkill", 2958, 2966),
    ("bjoblog", 2967, 2987),
    ("bjobs", 2988, 2996),
    ("bjob_send_data", 2997, 3007),
    ("bjump", 3008, 3023),
    ("bkerberos_ccache_use", 3024, 3034),
    ("bkerberos_ticket_purge", 3035, 3044),
    ("bkerberos_ticket_use", 3045, 3055),
    ("bkeylogger", 3056, 3067),
    ("bkill", 3068, 3076),
    ("blink", 3077, 3088),
    ("blog", 3089, 3099),
    ("blog2", 3100, 3110),
    ("bloginuser", 3111, 3131),
    ("blogonpasswords", 3132, 3146),
    ("bls", 3147, 3161),
    ("bmimikatz", 3162, 3174),
    ("bmimikatz_small", 3175, 3192),
    ("bmkdir", 3193, 3201),
    ("bmode", 3202, 3213),
    ("bmv", 3214, 3223),
    ("bnet", 3224, 3308),
    ("bnote", 3309, 3317),
    ("bof_extract", 3318, 3336),
    ("bof_pack", 3337, 3392),
    ("bpassthehash", 3393, 3407),
    ("bpause", 3408, 3418),
    ("bportscan", 3419, 3435),
    ("bpowerpick", 3436, 3452),
    ("bpowershell", 3453, 3466),
    ("bpowershell_import", 3467, 3479),
    ("bpowershell_import_clear", 3480, 3489),
    ("bppid", 3490, 3504),
    ("bprintscreen", 3505, 3516),
    ("bps", 3517, 3532),
    ("bpsexec", 3533, 3546),
    ("bpsexec_command", 3547, 3561),
    ("bpsexec_psh", 3562, 3565),
    ("bpsinject", 3566, 3577),
    ("bpwd", 3578, 3587),
    ("bread_pipe", 3588, 3603),
    ("breg_queryv", 3604, 3616),
    ("bremote_exec", 3630, 3645),
    ("brev2self", 3646, 3655),
    ("brm", 3656, 3665),
    ("brportfwd", 3666, 3676),
    ("brportfwd_local", 3677, 3687),
    ("brportfwd_stop", 3688, 3696),
    ("brun", 3697, 3709),
    ("brunas", 3710, 3721),
    ("brunasadmin", 3722, 3739),
    ("brunu", 3740, 3749),
    ("bscreenshot", 3750, 3764),
    ("bscreenwatch", 3765, 3779),
    ("bsetenv", 3780, 3792),
    ("bshell", 3793, 3804),
    ("bshinject", 3805, 3815),
    ("bshspawn", 3816, 3825),
    ("bsleep", 3826, 3838),
    ("bsleepu", 3839, 3859),
    ("bsocks", 3860, 3874),
    ("bsocks_stop", 3875, 3884),
    ("bspawn", 3885, 3899),
    ("bspawnas", 3900, 3911),
    ("bspawnto", 3912, 3932),
    ("bspawnu", 3933, 3942),
    ("bspunnel", 3943, 3954),
    ("bspunnel_local", 3955, 3966),
    ("bssh", 3967, 3982),
    ("bssh_key", 3983, 3995),
    ("bstage", 3996, 3999),
    ("bsteal_token", 4000, 4020),
    ("bsudo", 4021, 4033),
    ("bsyscall_method", 4034, 4052),
    ("btask", 4053, 4066),
    ("btimestomp", 4067, 4082),
    ("btoken_store_remove", 4083, 4091),
    ("btoken_store_remove_all", 4092, 4099),
    ("btoken_store_show", 4100, 4107),
    ("btoken_store_steal", 4108, 4117),
    ("btoken_store_steal_and_use", 4118, 4127),
    ("btoken_store_use", 4128, 4136),
    ("bunlink", 4137, 4146),
    ("bupload", 4147, 4155),
    ("bupload_raw", 4156, 4165),
    ("bwdigest", 4166, 4169),
    ("bwinrm", 4170, 4173),
    ("bwmi", 4174, 4179),
    ("call", 4180, 4189),
    ("closeClient", 4190, 4195),
    ("colorMenu", 4196, 4211),
    ("credential_add", 4212, 4227),
    ("credentials", 4228, 4235),
    ("custom_event", 4236, 4244),
    ("custom_event_private", 4245, 4254),
    ("data_keys", 4255, 4265),
    ("data_query", 4266, 4275),
    ("dbutton_action", 4276, 4285),
    ("dbutton_help", 4286, 4294),
    ("dialog", 4295, 4315),
    ("dialog_description", 4316, 4325),
    ("dialog_show", 4326, 4333),
    ("dispatch_event", 4334, 4343),
    ("downloads", 4344, 4351),
    ("drow_beacon", 4352, 4361),
    ("drow_checkbox", 4362, 4372),
    ("drow_combobox", 4373, 4383),
    ("drow_exploits", 4384, 4393),
    ("drow_file", 4394, 4403),
    ("drow_interface", 4404, 4413),
    ("drow_krbtgt", 4414, 4423),
    ("drow_listener", 4424, 4433),
    ("drow_listener_smb", 4434, 4439),
    ("drow_listener_stage", 4440, 4449),
    ("drow_mailserver", 4450, 4459),
    ("drow_proxyserver", 4460, 4471),
    ("drow_site", 4472, 4481),
    ("drow_text", 4482, 4492),
    ("drow_text_big", 4493, 4502),
    ("dstamp", 4503, 4513),
    ("elog", 4514, 4521),
    ("encode", 4522, 4564),
    ("extract_reflective_loader", 4565, 4579),
    ("file_browser", 4580, 4584),
    ("fireAlias", 4585, 4597),
    ("fireEvent", 4598, 4610),
    ("format_size", 4611, 4620),
    ("getAggressorClient", 4621, 4626),
    ("getAggressorClientType", 4627, 4639),
    ("get_postex_kit_callback_id", 4640, 4649),
    ("gunzip", 4650, 4662),
    ("gzip", 4663, 4675),
    ("highlight", 4676, 4740),
    ("host_delete", 4741, 4749),
    ("host_info", 4750, 4767),
    ("host_update", 4768, 4781),
    ("hosts", 4782, 4789),
    ("insert_color_menu", 4790, 4804),
    ("insert_component", 4805, 4811),
    ("insert_menu", 4812, 4826),
    ("iprange", 4827, 4870),
    ("keystrokes", 4871, 4878),
    ("killdate", 4879, 4899),
    ("listener_create", 4900, 4920),
    ("listener_create_ext", 4921, 5224),
    ("listener_delete", 5225, 5232),
    ("listener_describe", 5233, 5245),
    ("listener_info", 5246, 5263),
    ("listener_pivot_create", 5264, 5290),
    ("listener_restart", 5291, 5298),
    ("listeners", 5299, 5306),
    ("listeners_local", 5307, 5314),
    ("listeners_stageless", 5315, 5322),
    ("localip", 5323, 5330),
    ("menubar", 5331, 5344),
    ("mynick", 5345, 5352),
    ("nextTab", 5353, 5360),
    ("on", 5361, 5373),
    ("openAboutDialog", 5374, 5379),
    ("openApplicationManager", 5380, 5385),
    ("openAutoRunDialog", 5386, 5391),
    ("openBeaconBrowser", 5392, 5397),
    ("openBeaconConsole", 5398, 5410),
    ("openBrowserPivotSetup", 5411, 5423),
    ("openBypassUACDialog", 5424, 5428),
    ("openCloneSiteDialog", 5429, 5434),
    ("openConnectDialog", 5435, 5440),
    ("openCovertVPNSetup", 5441, 5453),
    ("openCredentialManager", 5454, 5459),
    ("openDefaultShortcutsDialog", 5460, 5464),
    ("openDownloadBrowser", 5465, 5470),
    ("openElevateDialog", 5471, 5483),
    ("openEventLog", 5484, 5499),
    ("openFileBrowser", 5500, 5512),
    ("openGoldenTicketDialog", 5513, 5525),
    ("openHTMLApplicationDialog", 5526, 5531),
    ("openHostFileDialog", 5532, 5537),
    ("openInterfaceManager", 5538, 5543),
    ("openJavaSignedAppletDialog", 5544, 5549),
    ("openJavaSmartAppletDialog", 5550, 5555),
    ("openJobBrowser", 5556, 5565),
    ("openJobConsole", 5566, 5573),
    ("openJumpDialog", 5574, 5582),
    ("openKeystrokeBrowser", 5583, 5588),
    ("openListenerManager", 5589, 5594),
    ("openMakeTokenDialog", 5595, 5607),
    ("openMalleableProfileDialog", 5608, 5613),
    ("openOfficeMacroDialog", 5614, 5619),
    ("openOneLinerDialog", 5620, 5629),
    ("openOrActivate", 5630, 5642),
    ("openPayloadGeneratorDialog", 5643, 5648),
    ("openPayloadGeneratorStageDialog", 5649, 5654),
    ("openPayloadHelper", 5655, 5664),
    ("openPivotListenerSetup", 5665, 5677),
    ("openPortScanner", 5678, 5685),
    ("openPortScannerLocal", 5686, 5698),
    ("openPowerShellWebDialog", 5699, 5704),
    ("openPreferencesDialog", 5705, 5710),
    ("openProcessBrowser", 5711, 5720),
    ("openSOCKSBrowser", 5721, 5726),
    ("openSOCKSSetup", 5727, 5739),
    ("openScreenshotBrowser", 5740, 5745),
    ("openScriptConsole", 5746, 5760),
    ("openScriptManager", 5761, 5766),
    ("openScriptedWebDialog", 5767, 5772),
    ("openServiceBrowser", 5773, 5780),
    ("openSiteManager", 5781, 5786),
    ("openSpawnAsDialog", 5787, 5799),
    ("openSpawnDialog", 5800, 5807),
    ("openSpearPhishDialog", 5808, 5813),
    ("openSystemInformationDialog", 5814, 5819),
    ("openSystemProfilerDialog", 5820, 5825),
    ("openTargetBrowser", 5826, 5831),
    ("openWebLog", 5832, 5847),
    ("openWindowsDropperDialog", 5848, 5851),
    ("openWindowsExecutableDialog", 5852, 5857),
    ("openWindowsExecutableStageDialog", 5858, 5863),
    ("openWindowsExecutableStageAllDialog", 5864, 5869),
    ("payload", 5870, 5895),
    ("payload_bootstrap_hint", 5896, 5910),
    ("payload_local", 5911, 5936),
    ("pe_insert_rich_header", 5937, 5953),
    ("pe_mask", 5954, 6024),
    ("pe_mask_section", 6025, 6073),
    ("pe_mask_string", 6074, 6137),
    ("pe_patch_code", 6138, 6179),
    ("pe_remove_rich_header", 6180, 6192),
    ("pe_set_compile_time_with_long", 6193, 6209),
    ("pe_set_compile_time_with_string", 6210, 6222),
    ("pe_set_export_name", 6223, 6241),
    ("pe_set_long", 6242, 6304),
    ("pe_set_short", 6305, 6367),
    ("pe_set_string", 6368, 6430),
    ("pe_set_stringz", 6431, 6503),
    ("pe_set_value_at", 6504, 6578),
    ("pe_stomp", 6579, 6639),
    ("pe_update_checksum", 6640, 6654),
    ("pedump", 6655, 6710),
    ("pgraph", 6711, 6721),
    ("pivots", 6722, 6729),
    ("pi_explicit_get", 6730, 6737),
    ("pi_explicit_info", 6738, 6745),
    ("pi_explicit_set", 6746, 6753),
    ("pi_spawn_get", 6754, 6761),
    ("pi_spawn_info", 6762, 6769),
    ("pi_spawn_set", 6770, 6777),
    ("pi_user_explicit_clear", 6778, 6783),
    ("pi_user_spawn_clear", 6784, 6789),
    ("pi_user_explicit_get", 6790, 6797),
    ("pi_user_explicit_get_map", 6798, 6803),
    ("pi_user_explicit_get_names", 6804, 6809),
    ("pi_user_explicit_set", 6810, 6817),
    ("pi_user_spawn_get", 6818, 6825),
    ("pi_user_spawn_get_map", 6826, 6831),
    ("pi_user_spawn_get_names", 6832, 6837),
    ("pi_user_spawn_set", 6838, 6845),
    ("popup_clear", 6846, 6859),
    ("powershell", 6860, 6875),
    ("powershell_command", 6876, 6887),
    ("powershell_compress", 6888, 6895),
    ("pref_get", 6896, 6906),
    ("pref_get_list", 6907, 6916),
    ("pref_set", 6917, 6925),
    ("pref_set_list", 6926, 6934),
    ("previousTab", 6935, 6942),
    ("process_browser", 6943, 6947),
    ("privmsg", 6948, 6956),
    ("prompt_confirm", 6957, 6968),
    ("prompt_directory_open", 6969, 6981),
    ("prompt_file_open", 6982, 6994),
    ("prompt_file_save", 6995, 7008),
    ("prompt_text", 7009, 7020),
    ("range", 7021, 7056),
    ("redactobject", 7057, 7063),
    ("removeTab", 7064, 7071),
    ("resetData", 7072, 7076),
    ("say", 7077, 7084),
    ("sbrowser", 7085, 7095),
    ("screenshots", 7096, 7103),
    ("script_resource", 7104, 7113),
    ("separator", 7114, 7123),
    ("services", 7124, 7131),
    ("setup_reflective_loader", 7132, 7149),
    ("setup_strings", 7150, 7161),
    ("setup_transformations", 7162, 7174),
    ("shellcode", 7175, 7194),
    ("showVisualization", 7195, 7207),
    ("show_error", 7208, 7215),
    ("show_message", 7216, 7223),
    ("site_host", 7224, 7239),
    ("site_kill", 7240, 7249),
    ("sites", 7250, 7257),
    ("ssh_command_describe", 7258, 7267),
    ("ssh_command_detail", 7268, 7279),
    ("ssh_command_group", 7280, 7308),
    ("ssh_command_register", 7309, 7333),
    ("ssh_commands", 7334, 7341),
    ("stager", 7342, 7358),
    ("stager_bind_pipe", 7359, 7380),
    ("stager_bind_tcp", 7381, 7404),
    ("str_chunk", 7405, 7420),
    ("str_decode", 7421, 7432),
    ("str_encode", 7433, 7444),
    ("str_xor", 7445, 7456),
    ("sync_download", 7457, 7476),
    ("targets", 7477, 7484),
    ("tbrowser", 7485, 7495),
    ("tokenToEmail", 7496, 7513),
    ("transform", 7514, 7562),
    ("transform_vbs", 7563, 7581),
    ("tstamp", 7582, 7592),
    ("unbind", 7593, 7605),
    ("url_open", 7606, 7615),
    ("users", 7616, 7625),
    ("vpn_interface_info", 7626, 7643),
    ("vpn_interfaces", 7644, 7651),
    ("vpn_tap_create", 7652, 7663),
    ("vpn_tap_delete", 7664, 7691),
]


class HTMLToMarkdownConverter(HTMLParser):
    """Simple HTML to Markdown converter for function documentation."""

    def __init__(self):
        super().__init__()
        self.markdown = []
        self.in_pre = False
        self.in_code = False
        self.in_p = False
        self.in_li = False
        self.in_table = False
        self.in_th = False
        self.in_td = False
        self.table_rows = []
        self.current_row = []
        self.list_indent = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            # Extract function name from id attribute
            for attr, value in attrs:
                if attr == 'id':
                    self.markdown.append(f"# {value}\n\n")
        elif tag == 'h3':
            self.markdown.append("### ")
        elif tag == 'h4':
            self.markdown.append("#### ")
        elif tag == 'p':
            self.in_p = True
        elif tag == 'pre':
            self.in_pre = True
            self.markdown.append("```\n")
        elif tag == 'code' and not self.in_pre:
            self.in_code = True
            self.markdown.append("`")
        elif tag == 'strong' or tag == 'b':
            self.markdown.append("**")
        elif tag == 'em' or tag == 'i':
            self.markdown.append("*")
        elif tag == 'ul':
            self.list_indent += 1
        elif tag == 'ol':
            self.list_indent += 1
        elif tag == 'li':
            self.in_li = True
            indent = "  " * (self.list_indent - 1)
            self.markdown.append(f"{indent}- ")
        elif tag == 'table':
            self.in_table = True
            self.table_rows = []
        elif tag == 'tr':
            self.current_row = []
        elif tag == 'th':
            self.in_th = True
        elif tag == 'td':
            self.in_td = True
        elif tag == 'br':
            self.markdown.append("\n")

    def handle_endtag(self, tag):
        if tag == 'h2' or tag == 'h3' or tag == 'h4':
            self.markdown.append("\n\n")
        elif tag == 'p':
            self.in_p = False
            self.markdown.append("\n\n")
        elif tag == 'pre':
            self.in_pre = False
            self.markdown.append("```\n\n")
        elif tag == 'code' and not self.in_pre:
            self.in_code = False
            self.markdown.append("`")
        elif tag == 'strong' or tag == 'b':
            self.markdown.append("**")
        elif tag == 'em' or tag == 'i':
            self.markdown.append("*")
        elif tag == 'ul' or tag == 'ol':
            self.list_indent -= 1
            if self.list_indent == 0:
                self.markdown.append("\n")
        elif tag == 'li':
            self.in_li = False
            self.markdown.append("\n")
        elif tag == 'th':
            self.in_th = False
            self.current_row.append("")
        elif tag == 'td':
            self.in_td = False
            self.current_row.append("")
        elif tag == 'tr':
            if self.current_row:
                self.table_rows.append(self.current_row[:])
        elif tag == 'table':
            self.in_table = False
            if self.table_rows:
                # Format as markdown table
                for i, row in enumerate(self.table_rows):
                    self.markdown.append("| " + " | ".join(row) + " |\n")
                    if i == 0:  # Add separator after header
                        self.markdown.append("| " + " | ".join(["---"] * len(row)) + " |\n")
                self.markdown.append("\n")

    def handle_data(self, data):
        # Clean up whitespace
        if self.in_pre:
            self.markdown.append(data)
        else:
            data = re.sub(r'\s+', ' ', data)
            if data.strip():
                if self.in_th or self.in_td:
                    if self.current_row:
                        self.current_row[-1] += data.strip()
                else:
                    self.markdown.append(data)

    def get_markdown(self):
        return ''.join(self.markdown).strip()


def extract_function_html(html_file, start_line, end_line):
    """Extract HTML content between start and end lines."""
    with open(html_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Line numbers are 1-indexed
    return ''.join(lines[start_line - 1:end_line])


def html_to_markdown(html_content):
    """Convert HTML content to Markdown."""
    converter = HTMLToMarkdownConverter()
    converter.feed(html_content)
    return converter.get_markdown()


def main():
    """Main extraction function."""
    html_file = "/Users/xpn/.local/share/opencode/tool-output/tool_c488a1bf500191l26Tt8gBq3bE"
    output_dir = Path("/Users/xpn/.claude/skills/skills/aggressor/references/aggressor-functions")

    print(f"Extracting {len(FUNCTIONS)} functions...")

    for func_name, start_line, end_line in FUNCTIONS:
        # Create lowercase filename
        filename = f"{func_name.lower()}.md"
        output_path = output_dir / filename

        # Extract HTML for this function
        html_content = extract_function_html(html_file, start_line, end_line)

        # Convert to Markdown
        markdown_content = html_to_markdown(html_content)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"Created: {filename}")

    print(f"\nSuccessfully extracted {len(FUNCTIONS)} function documentation files!")


if __name__ == "__main__":
    main()
