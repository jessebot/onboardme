require ["include", "environment", "variables", "relational", "comparator-i;ascii-numeric", "spamtest"];
require ["fileinto", "imap4flags"];

# Generated: Do not run this script on spam messages
if allof (environment :matches "vnd.proton.spam-threshold" "*", spamtest :value "ge" :comparator "i;ascii-numeric" "${1}") {
    return;
}

/**
 * @type or
 * @comparator contains
 */
if anyof (header :comparator "i;unicode-casemap" :contains "Subject" ["Receipt", "your order"]) {
    fileinto "Receipts";
}
