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
if allof (header :comparator "i;unicode-casemap" :contains "Subject" ["Bedankt voor je bestelling bij", "Thank you for your order", "Your order's in the kitchen", "Bevestiging van uw bestelling bij Full Moon Garden"], address :all :comparator "i;unicode-casemap" :contains "From" ["no-reply@thuisbezorgd.nl", "noreply@t.deliveroo.com", "noreply@sitedish.nl", "thuisbezorgd.nl"]) {
    fileinto "Purchases/Food/Eating Out";
    addflag "\\Seen";
    keep;
}
