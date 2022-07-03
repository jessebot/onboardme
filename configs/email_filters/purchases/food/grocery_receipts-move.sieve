require ["include", "environment", "variables", "relational", "comparator-i;ascii-numeric", "spamtest"];
require ["fileinto", "imap4flags"];

# Generated: Do not run this script on spam messages
if allof (environment :matches "vnd.proton.spam-threshold" "*", spamtest :value "ge" :comparator "i;ascii-numeric" "${1}") {
    return;
}

/**
 * @type and
 * @comparator contains
 * @comparator contains
 */
if allof (header :comparator "i;unicode-casemap" :contains "Subject" ["digitale bon", "Factuur voor uw De Notenshop bestelling", "Uw De Notenshop bestelbevestiging"], address :all :comparator "i;unicode-casemap" :contains "From" ["jumbo@service.jumbo.com", "info@denotenshop.nl"]) {
    fileinto "Food/Groceries";
    addflag "\\Seen";
    keep;
}
