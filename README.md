# Personal Rolling Budget

This is a command-line based tool that can compute how much you spend during the
last four weeks on a rolling basis, instead of just taking the current month.
While this approach has some drawbacks (for example, it makes it harder to
budget big expenses), it allows to precisely control your budget, as it always show what you have spent in the last 4 weeks. That way, you don't have to be
at the end of the month to see that you've spent too much. You can control your
spending every day precisely.

The tools bases on CSV data, so this could be fed by a Dropbox-hosted file as
well. An example to the CSV data will be delivered as a template.

The code is still being finalized for release. Keep watching and thanks for
your interest.

## Run The tool

Update the filename of expenses2016.csv so that it reflects the current year
and month (`expensesYYYYMM.csv`). Also update the dates _inside_ the file so
they are no longer than 28 days old.

```shell
0> python budget.py
Reporting budget use from the last running 4 weeks compared to the set budget

Processing expenses201610.csv... ✓

Compute budget...
Expenses from last 4 weeks of 90.0EUR
```

## Known Limitations

- It operates on a four week basis, not on a full month.
- It only works with EURO currency so far.
- No changeable budget limit to check against.
