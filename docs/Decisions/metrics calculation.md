## Goal
The naive metrics pipeline helps us compare different hypotheses and run sanity checks. It does not replace user feedback, but it gives us a quick way to understand which variant performs better.

## Overview
The metrics module has two parts: generation and execution.  
The generation part creates synthetic test cases: it builds a menu, participants, reference assignments, a bill image mock, and a user message.  
The execution part runs the current model on these test cases and computes metrics.

## Generation module
The generation module tries to recreate the user flow and produce reference data.

- Menu creation - we assign random prices to the meals in our menu.
- Participant creation - we randomly choose the number of participants and generate their names. Then we store them as `User` objects.
- Reference assignment - we randomly assign meals from the menu to participants and store the result as a `Receipt`.
- Bill creation - we create a synthetic bill that mimics the photo a user would send to the model.
- User message generation - we use an LLM to generate a user message based on the data created above.
- Serialization - we write each generated test case to a JSONL file.

## Execution module
In the execution module, we use previously generated tests to evaluate our current model.

We calculate metrics both for the whole test set and for each item, so we can clearly understand which types of requests our model struggles with.

We currently compute the following metrics:
* for each item: price MAE, detected users F1
* for each user in an item: meals total, missing, extra, and price MAE
* summary: price MAE, price MAPE, detected users F1, assigned meals F1, mean input tokens, mean output tokens