require ["include", "environment", "variables", "relational", "comparator-i;ascii-numeric", "spamtest"];
require ["fileinto", "imap4flags"];

# Generated: Do not run this script on spam messages
if allof (environment :matches "vnd.proton.spam-threshold" "*", spamtest :value "ge" :comparator "i;ascii-numeric" "${1}") {
    return;
}

# Bol.com receipts - Mark: Read / Move to: Purchases/bol.com
/**
 * @type and
 * @comparator contains
 * @comparator contains
 */
if allof (header :comparator "i;unicode-casemap" :contains "Subject" ["Factuur Bestelling", "Bedankt voor je bestelling met bestelnummer", "Factuur voor uw"], address :all :comparator "i;unicode-casemap" :contains "From" "bol.com") {
    fileinto "Purchases/bol.com";
    addflag "\\Seen";
    keep;
}
