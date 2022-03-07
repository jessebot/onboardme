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
if anyof (address :all :comparator "i;unicode-casemap" :contains "From" ["notify.protonmail.com", "notifications@github.com", "service@paypal.nl", "adamdoctors.nl", "wise.com", "payments-noreply@google.com", "workspace-noreply@google.com", "deel.support", "members@medium.com", "bunq.com", "ziggo.com", "ziggo.nl", "bitwarden.com"]) {
    fileinto "Providers";
}

