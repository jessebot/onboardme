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
if anyof (header :comparator "i;unicode-casemap" :contains "Subject" "\"verify your\"", address :all :comparator "i;unicode-casemap" :contains "From" "no-reply@accounts.google.com") {
    fileinto "Security";
}
