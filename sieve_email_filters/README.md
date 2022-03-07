# Sieve Filter Scripts
I can't believe I didn't just standardize these so I can burn emails at will. Live and learn.

Anyway, here you'll find some basic filters to categorize the mundane adult stuff when you move to a new email provider or start hosting your own :)

I live in the Netherlands, so some of the filters contain dutch domains and phrases.

# But What is Sieve though?
TLDR; Sieve is a programming language used to filter emails.

You can read more about it on [Wikipedia](https://en.wikipedia.org/wiki/Sieve_(mail_filtering_language)) and Proton's support page has a pretty good breakdown [here](https://protonmail.com/support/knowledge-base/sieve-advanced-custom-filters/)

# Current (Jesse) Categorical Filters

**NOTE**: *Unless otherwise noted, all these filters will mark every email as read.*

## Delivery Updates
Script: [delivery_updates-label_delete.sieve](delivery_updates-label_delete.sieve)
|                          Sites                         	|                      Move/Label                     	    |
|:------------------------------------------------------	|:-------------------------------------------------------:	|
| **Food**: Thuisbezorgd, Deliveroo<br>**Misc**: bol.com 	| Labels `Delivery Updates` **and** Moves to `Trash`.       |


## Review Requests and Stampcard updates
Script: [review_requests-delete.sieve](review_requests-delete.sieve)
|                          Sites                                    	|                      Move/Label                	|
|:------------------------------------------------------------------	|:------------------------------------------------:	|
| **Food**: Thuisbezorgd, Deliveroo<br>**Misc**: bol.com, fruugo.com 	| Labels `Review Requests` **and** Moves to `Trash`.|

## Food
### Eating Out (Delivery, Takeout) Reciepts
Script: [food-eating_out_receipts-move.sieve](food-eating_out_receipts-move.sieve)
|       Sites               |                   Move/Label              	|
|:-------------------------	|:---------------------------------------------:|
| Thuisbezorgd, Deliveroo 	| Moves to folder, `Purchases/Food/Eating Out`. |

### Online Grocery Order Reciepts
Script: [food-grocery_receipts-move.sieve](food-grocery_receipts-move.sieve)
|       Sites               |                   Move/Label                 	|
|:-------------------------	|:---------------------------------------------:|
| Jumbo, denotenshop.nl   	| Moves to folder, `Purchases/Food/Groceries`.  |

### bol.com Receipts
Script: [bol_com_receipts-move.sieve](bol_com_receipts-move.sieve)
Moves to folder, `Purchases/bol.com`


# Current Max added Categorical Filters :D

1. Sort Appointments

    Attempts to find emials with appointmnt information and move them to an `Appointments` folder.

    [sort_appointments](sort_appointmwnts.sieve)

<br>

2. Sort Job Spam

    Attempts to find auto-generated job recruitment emails and move them to the `Spam` folder.

    [sort_job_spam](sort_job_spam.sieve)

    <br>

3. Sort Appointments

    Forwards credible job opportunities to a `Job Mail` folder.

    [sort_jobs_to_folder](sort_jobs_to_folder.sieve)

    <br>

4. Sort Providers

    Forwards emails from trusted/important companies/services to a `Providers` folder.
    
    [sort_providers_to_folder](sort_jobs_to_folder.sieve)

5. Sort Appointments

    Forwards credible job opportunities to a `Job Mail` folder.
    
    [sort_jobs_to_folder](sort_jobs_to_folder.sieve)