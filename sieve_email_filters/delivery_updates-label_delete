require ["include", "environment", "variables", "relational", "comparator-i;ascii-numeric", "spamtest"];
require ["fileinto", "imap4flags"];

# Generated: Do not run this script on spam messages
if allof (environment :matches "vnd.proton.spam-threshold" "*", spamtest :value "ge" :comparator "i;ascii-numeric" "${1}") {
    return;
}

# Delivery Updates - Label: Delivery Updates / Mark: Read / Move: Trash
/**
 * @type and
 * @comparator contains
 */
if allof (header :comparator "i;unicode-casemap" :contains "Subject" ["is shipped", "Shipping Confirmation", "klaar voor verzending", "bestelling ontvangen", "is in transit", "over uw zending", "packing your order", "bezorgd", "verzonden", "out for delivery", "delivered", "ingepakt", "onderweg", "geleverd"]) {
    fileinto "trash";
    fileinto "Delivery Updates";
    addflag "\\Seen";
    keep;
}
