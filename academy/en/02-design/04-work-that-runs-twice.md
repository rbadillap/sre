---
title: "Work that runs twice"
stage: design
order: 4
status: approved
teaches: "Find where work can run twice, give it a stable ID that makes a second run safe, and say where that can't be guaranteed."
sources:
  - title: "GitHub, Revenge of the double billing"
    url: https://github.blog/news-insights/the-library/revenge-of-the-double-billing/
  - title: "AuthVia, Post-Incident Report: October 14, 2025, Duplicate Payment Executions"
    url: https://status.authvia.com/incidents/3hzrsb96jhkh
  - title: "Stripe, Designing robust and predictable APIs with idempotency"
    url: https://stripe.com/blog/idempotency
  - title: "Amazon Builders' Library, Making retries safe with idempotent APIs"
    url: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
skills: [idempotency]
version: "0.1.1"
---

# Work that runs twice

_Sources: [GitHub's "Revenge of the double billing"](https://github.blog/news-insights/the-library/revenge-of-the-double-billing/), [AuthVia's report on October 14, 2025](https://status.authvia.com/incidents/3hzrsb96jhkh), [Stripe's post on idempotency](https://stripe.com/blog/idempotency), and [the Amazon Builders' Library article on idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)._

## The question

A job can run again, and a client that gets no answer doesn't know if its request worked. How do you make the second run safe?

## What happened at GitHub

GitHub's post is dated September 30, 2009.

- **The repeat.** "Monday morning's billing batch processed twice."
- **The first repair.** "As soon as we realized this we ran a batch to void the duplicate transactions." To void is to cancel a charge. "We thought this solved the issue, but we were wrong."
- **What it missed.** After a user reported being billed twice, GitHub found the void batch had missed "a small handful of users": those whose card "had declined in a previous batch and were being retried".
- **The second repair.** The author says they refunded those customers by hand. The post also asks everyone who received a receipt that Monday to check with their bank.

The post doesn't say why the batch ran twice, or how many customers were charged.

## What happened at AuthVia

AuthVia's service submits payments to gateways, the services that process them. All times are Pacific, on October 14, 2025.

- **07:30:** its status page said "some gateways are showing duplicate payments".
- **12:44:** it asked: "Please, if you are able, void the duplicate transactions in your gateway portal."

Its report, posted the next day, says that during a scheduled deployment "a logic change in our transaction workflow inadvertently caused certain payment requests to re-execute under specific timing conditions". It says "a limited number" of duplicates, and gives no count. It says it was working with partners and merchants to reverse the charges, and doesn't give the final result.

## What Stripe's post says

Stripe's post, from February 22, 2017, starts from a call between two machines. It lists three failures: the connection fails, the server fails partway, or the work succeeds and the answer is lost. In many cases the client can't tell whether a retry is safe.

- **Idempotent** means an endpoint can "be called any number of times while guaranteeing that side effects only occur once".
- **Some calls are naturally safe.** Its hypothetical DNS example sends everything needed to create a record. A repeat is ignored and gets a success status.
- **Others need a key.** Charging money is its example. The client generates a unique ID for the operation, called an idempotency key, sends it with the request, and retries with the same ID.
- **A repeat depends on the failure.** The server may process it for the first time, finish the work, or reply "with a cached result".

## What the AWS article says

- **Who sets the ID.** Treating identical parameters as a duplicate "doesn't work in all cases": a caller may really want two identical EC2 instances. Amazon prefers a "unique caller-provided client request identifier".
- **The ID and the work go together.** Recording the ID and making the changes must be one atomic operation, all or nothing. Otherwise the service could record the ID without creating the resources, or create them without recording the ID.
- **The answer matters too.** Replying `ResourceAlreadyExists` to a retry has no side effect on the service, but it changes what the caller has to do. Amazon gives a "semantically equivalent response": the same meaning, though "very similar but not identical", as an instance's state may have changed.
- **IDs don't last forever.** Keeping them indefinitely is "impractical". For EC2 instances, it keeps them for the life of the resource plus an interval for late requests.
- **Same ID, different parameters.** Amazon returns a validation error, and stores the original parameters to detect this.
- **It has a cost.** AWS says "there is cost and complexity inherent" and that the complexity "is not right for all solutions".

## Reading the cases

The rest of this lesson is its own reading and method. Neither GitHub nor AuthVia mentions idempotency keys, and neither says a key would have prevented the duplicates. Stripe and AWS describe designs and report no incident or before-and-after figures. So this lesson's sources don't show a key stopping a real duplicate.

- **Repeats aren't always a client's retry.** GitHub's repeat was a batch, though its post gives no cause. AuthVia's report points to a logic change. So look at the whole path, not only the client's retry loop.
- **A repair can miss cases too.** GitHub's void batch missed a group of customers. The post doesn't say why it missed them. This lesson's rule: build a repair from what actually happened, then check it afterwards.
- **Effects outside your system are the limit.** An atomic write can't include another company's system. If a provider accepts a key, as Stripe's API does, pass one. If it doesn't, and you can't ask the provider what happened, a crash at the wrong moment leaves a choice between a possible duplicate and a possible miss.

## How to do it

1. List everything that can run this work again: clients, proxies, queues, schedulers, and people rerunning a job.
2. Decide whether the work is naturally safe. If not, give it an ID, set by whoever creates the work.
3. Store the ID in the same atomic write as the result, with a uniqueness rule.
4. Decide what a repeat gets: the original result, or one with the same meaning, not a confusing error. If the parameters differ, reject it.
5. Keep IDs well past the longest time a repeat can arrive, and write down that time.
6. For each effect outside your system, pass a key if you can. If you can't, write which risk you chose.

## Worked example

An example written for this lesson. It borrows only GitHub's situation, a billing batch with retries for declined cards. It isn't how GitHub's system worked: the post doesn't say.

- **Unit of work:** one customer's bill for one month. **ID:** `customer-123/2026-10`, set when the bill is created.
- **Record:** one row per ID, with a uniqueness rule and a state: started, charged or declined.
- **Provider:** accepts no key.
- **The whole batch runs twice:** each ID already exists, so the second run starts no new charge and reports the existing state.
- **A declined card is retried:** the retry belongs to the same bill and runs only while the state is declined.
- **Crash after the provider charges, before the record is saved:** the state still says started. Check with the provider before charging again. The row is written before the charge because the provider can't share an atomic write. This is the case the ID can't guarantee.
- **Repair:** list bills with more than one successful charge from the provider's records, not from the batch's list. Count again afterwards.

_If you use rbadillap/sre: `idempotency` gives each unit of work a stable ID, stores it in the same write as the result behind a uniqueness constraint, and acknowledges only after the work is durable. It also makes you state where this can't be guaranteed, such as a provider without a key. A repeat is skipped: it doesn't cover returning the original result, or rejecting a changed request, as AWS does._

## In one sentence

"Anything that can run twice and isn't naturally safe gets an ID from whoever created the work, saved together with the result, so a second run changes nothing, and I write down where I can't guarantee that."

## Exercise

A hypothetical case: a worker reads messages from a queue and charges a customer $25 for each one, through a provider. Last month there were 40,000 messages, and 0.2% were delivered a second time. The worker has no protection against repeats. The longest delay the queue allows for a repeat is 14 days.

1. Assume each repeated message charged again. How many duplicate charges were there, and for how much money?
2. A teammate proposes this ID: a hash of customer, item and amount. A customer buys the same $25 item twice on purpose, five minutes apart. What happens? What ID would you use, and who sets it?
3. The team proposes keeping IDs for 7 days. What can happen to a message repeated on day 10? What period would you choose, and why?
4. From here, assume the team has added IDs. A message arrives with a known ID, but the amount is now $30 instead of $25. Following the AWS article, what does the service do?
5. Assume the provider accepts no key and has no way to look up a past charge. The worker charges, then crashes before saving the ID. What happens when the message comes back? Which two risks do you choose between?
6. Pick one job or API call in a system you work on or use. What can make it run twice, and what would a second run do today?

---

_Written with an AI assistant from the sources above._
