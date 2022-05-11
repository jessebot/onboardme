require ["include", "environment", "variables", "relational", "comparator-i;ascii-numeric", "spamtest"];
require ["fileinto", "imap4flags"];

# Generated: Do not run this script on spam messages
if allof (environment :matches "vnd.proton.spam-threshold" "*", spamtest :value "ge" :comparator "i;ascii-numeric" "${1}") {
    return;
}

/**
 * @type or
 * @comparator contains
 * @comparator contains
 */
if anyof (header :comparator "i;unicode-casemap" :contains "Subject" ["\"greetings of the day\"", "\"urgent requirement\"", "at Remote", "\"is shared with you\""], address :all :comparator "i;unicode-casemap" :contains "From" ["tanishasystems.com", "messages-noreply@linkedin.com", "aptask.com", "oorwindigital.com"]) {
    fileinto "spam";
}
