html_dct = {
    'start_form' : 'body > form',
    'country' : 'body > form > table > tbody > tr:nth-child(3) > td:nth-child(3) > select > option:nth-child(56)',
    'city' : 'body > form > table > tbody > tr:nth-child(4) > td:nth-child(3) > select > option:nth-child(2)',
    'submit_btn' : '//input[@type="submit"]',
    'make_app_form' : 'body > table.margin_top20 > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > p',
    'app_btn' : '//input[@value="Make Appointment!"]',
    'procedure_form' : 'body > form > table:nth-child(3)',
    'read_flag' : 'body > form > table:nth-child(9) > tbody > tr > td:nth-child(1) > input',
    'calendar_form' : '#Form1',
}


procs_dct = {
    'Passport services other than adding pages': 'body > form > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(1) > input',
    "Report the birth abroad of a child of a U.S. citizen and/or apply for the child's first passport": 'body > form > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(1) > input',
    'Request notarial and other services not listed above': 'body > form > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(1) > input',
}


month_dct = {
    'January': '#Select1 > option:nth-child(1)',
    'February': '#Select1 > option:nth-child(2)',
    'March': '#Select1 > option:nth-child(3)',
    'April': '#Select1 > option:nth-child(4)',
    'May': '#Select1 > option:nth-child(5)',
    'June': '#Select1 > option:nth-child(6)',
    'July': '#Select1 > option:nth-child(7)',
    'August': '#Select1 > option:nth-child(8)',
    'September': '#Select1 > option:nth-child(9)',
    'October': '#Select1 > option:nth-child(10)',
    'November': '#Select1 > option:nth-child(11)',
    'December': '#Select1 > option:nth-child(12)',
}
