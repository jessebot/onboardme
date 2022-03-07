# Sieve Filter Scripts
I can't believe I didn't just standardize these so I can burn emails at will. Live and learn.

Anyway, here you'll find some basic filters to categorize the mundane adult stuff when you move to a new email provider or start hosting your own :)

I live in the Netherlands, so some of the filters contain dutch domains and phrases.

#### But What is Sieve though?
TLDR; Sieve is a programming language used to filter emails.
You can read more about it on [Wikipedia](https://en.wikipedia.org/wiki/Sieve_(mail_filtering_language)) and Proton's support page has a pretty good breakdown [here](https://protonmail.com/support/knowledge-base/sieve-advanced-custom-filters/).


# Current Categorical Filters

**NOTE**: *Unless otherwise noted, all these filters will mark every email as read.

## Delivery Updates
Script: [delivery_updates-label_delete](delivery_updates-label_delete)
|                          Sites                         	|                      Move/Label                     	    |
|:------------------------------------------------------	|:-------------------------------------------------------:	|
| **Food**: Thuisbezorgd, Deliveroo<br>**Misc**: bol.com 	| Labels `Delivery Updates` **and** Moves to `Trash`.       |


## Review Requests and Stampcard updates
Script: [review_requests-delete](review_requests-delete)
|                          Sites                                    	|                      Move/Label                	|
|:------------------------------------------------------------------	|:------------------------------------------------:	|
| **Food**: Thuisbezorgd, Deliveroo<br>**Misc**: bol.com, fruugo.com 	| Labels `Review Requests` **and** Moves to `Trash`.|

## Food
### Eating Out (Delivery, Takeout) Reciepts
Script: [food-eating_out_receipts-move](food-eating_out_receipts-move)
|       Sites               |                   Move/Label              	|
|:-------------------------	|:---------------------------------------------:|
| Thuisbezorgd, Deliveroo 	| Moves to folder, `Purchases/Food/Eating Out`. |

### Online Grocery Order Reciepts
Script: [food-grocery_receipts-move](food-grocery_receipts-move)
|       Sites               |                   Move/Label                 	|
|:-------------------------	|:---------------------------------------------:|
| Jumbo, denotenshop.nl   	| Moves to folder, `Purchases/Food/Groceries`.  |
