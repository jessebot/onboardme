# Sieve Filter Scripts
I can't believe I didn't just standardize these so I can burn emails at will. Live and learn.

Anyway, here you'll find some basic filters to categorize the mundane adult stuff when you move to a new email provider or start hosting your own :)

I live in the Netherlands, so some of the filters contain dutch domains and phrases.

### But What is Sieve though?
TLDR; Sieve is a programming language used to filter emails.

You can read more about it on [Wikipedia](https://en.wikipedia.org/wiki/Sieve_(mail_filtering_language)) and Proton's support page has a pretty good breakdown [here](https://protonmail.com/support/knowledge-base/sieve-advanced-custom-filters/)

# Current Categorical Filters

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
Script: [eating_out_receipts-move.sieve](food/eating_out_receipts-move.sieve)
|       Sites               |                   Move/Label              	|
|:-------------------------	|:---------------------------------------------:|
| Thuisbezorgd, Deliveroo 	| Moves to folder, `Purchases/Food/Eating Out`. |

### Online Grocery Order Reciepts
Script: [grocery_receipts-move.sieve](food/grocery_receipts-move.sieve)
|       Sites               |                   Move/Label                 	|
|:-------------------------	|:---------------------------------------------:|
| Jumbo, denotenshop.nl   	| Moves to folder, `Purchases/Food/Groceries`.  |

### bol.com Receipts
Script: [bol_com_receipts-move.sieve](bol_com_receipts-move.sieve)
Moves to folder, `Purchases/bol.com`


# Current Max added Categorical Filters :D

### Appointments
Script: [sort_appointments](sort_appointmwnts.sieve)
|       Sites   |            Move/Label             |
|:-------------	|:---------------------------------:|
| someguys  	| Moves to folder, `Appointments`.  |

## Jobs

## Jobs Spam
Script: [sort_job_spam](jobs/sort_job_spam.sieve)
Attempts to find auto-generated job recruitment emails and move them to the `Spam` folder.
|       Sites   |       Move/Label  |
|:-------------	|:-----------------:|
| someguys  	| Moves to `Spam`.  |

## Jobs Folder thing?
Script: [sort_jobs_to_folder](jobs/sort_jobs_to_folder.sieve)
Forwards credible job opportunities to a `Job Mail` folder. Change to Jobs/Recruitment/Credible ? :shrug:
|       Sites   |       Move/Label        |
|:-------------	|:-----------------------:|
| someenbies  	| Moves to `Recruiters`.  |

## Sort Providers?? ... also jobs hting?
Script: [sort_providers_to_folder](jobs/sort_jobs_to_folder.sieve) ??
Forwards emails from trusted/important companies/services to a `Providers` folder. ?? how is this different from above? :thinking:
|       Sites   |       Move/Label        |
|:-------------	|:-----------------------:|
| someenbies  	| Moves to `Recruiters`.  |
