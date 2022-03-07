# Product/Service Review Requests/Stamp Card updates - Delete
require ["include", "environment", "variables", "relational", "comparator-i;ascii-numeric", "spamtest"];
require ["fileinto", "imap4flags"];

# Generated: Do not run this script on spam messages
if allof (environment :matches "vnd.proton.spam-threshold" "*", spamtest :value "ge" :comparator "i;ascii-numeric" "${1}") {
    return;
}

/**
 * @type and
 * @comparator contains
 * @comparator ends
 */
if allof (header :comparator "i;unicode-casemap" :contains "Subject" ["Hoe was je ervaring met winkelen", "Je hebt je 1e stempel van", "We horen graag van je", "What do you think of your", "Wat vond je van je bestelling"], address :all :comparator "i;unicode-casemap" :matches "From" ["*fruugo.com", "*verkopen.bol.com", "*feedback.deliveroo.com", "*thuisbezorgd.nl"]) {
    fileinto "trash";
    fileinto "Review Requests";
    addflag "\\Seen";
    keep;
}
