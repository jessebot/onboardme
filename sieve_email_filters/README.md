# Sieve Filter Scripts
I can't believe I didn't just standardize these so I can burn emails at will. Live and learn.

Anyway, here you'll find some basic filters to categorize the mundane adult stuff when you move to a new email provider or start hosting your own :)

I live in the Netherlands, so some of the filters contain dutch domains and phrases.

## Current Categorical Filters

List of filters

1. Delivery Updates

    Applies label `Delivery Updates` and moves to Trash.

    [delivery_updates-label_delete](delivery_updates-label_delete.sieve)

    - Applicable Websites:

        > Currently covers the following domains:
        >
        >    * Food: Thuisbezorgd, Deliveroo
        >    * Misc: bol.com

</br>

2. Review Requests and Stampcard updates

    Applies label `Review Requests` and moves to Trash.

    [review_requests-delete](review_requests-delete.sieve)

    - Applicable Websites
        
        > Currently covers the following domains:
        >
        >   * Food: Thuisbezorgd, Deliveroo
        >   * Misc: bol.com, fruugo.com

</br>

3. Sort Appointments

    Attempts to find emials with appointmnt information and move them to an `Appointments` folder.

    [sort_appointments](sort_appointmwnts.sieve)

<br>

4. Sort Job Spam

    Attempts to find auto-generated job recruitment emails and move them to the `Spam` folder.

    [sort_job_spam](sort_job_spam.sieve)

    <br>

5. Sort Appointments

    Forwards credible job opportunities to a `Job Mail` folder.

    [sort_jobs_to_folder](sort_jobs_to_folder.sieve)

    <br>

6. Sort Providers

    Forwards emails from trusted/important companies/services to a `Providers` folder.
    
    [sort_providers_to_folder](sort_jobs_to_folder.sieve)

7. Sort Appointments

    Forwards credible job opportunities to a `Job Mail` folder.
    
    [sort_jobs_to_folder](sort_jobs_to_folder.sieve)





# But What is Sieve though?
TLDR; Sieve is a programming language used to filter emails.

You can read more about it on [Wikipedia](https://en.wikipedia.org/wiki/Sieve_(mail_filtering_language)) and Proton's support page has a pretty good breakdown [here](https://protonmail.com/support/knowledge-base/sieve-advanced-custom-filters/)
