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
if anyof (address :all :comparator "i;unicode-casemap" :contains "From" ["hit-reply@linkedin.com", "invitations@linkedin.com", "messaging-digest-noreply@linkedin.com", "offerzen.com", "orange-quarter.com"], header :comparator "i;unicode-casemap" :contains "Subject" "via LinkedIn") {
    fileinto "Job Mail";
}

