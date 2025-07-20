SBY configuration FAQs
----------------------

Choosing an engine and solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** How do I know which formal engine and/or which solver to use for
verifying my design?

**A:** Different combinations of engine and solver will perform differently and
may support different features or functionalities.  The :external+sby:ref:`SBY
engines reference <engines section>` lists all currently supported engines,
their options, available solvers, and which modes they operate in.  At this
time, a comprehensive comparison of when to use different engines/solvers is not
yet available.

With the introduction of the ``--autotune`` option it is now possible to
automatically compare available engines for a given SBY task.  Autotune will run
each engine, providing a report of time taken and the status returned.  This can
be used to quickly determine the fastest configuration while continuing to
iterate on a design. Check out the :external+sby:doc:`autotune docs <autotune>`
for more information.


Tool runtime
^^^^^^^^^^^^

**Q:** How long do I have to wait for SBY to complete?  For example, running one
of the examples included with the tool didn't appear to be making any progress
even after half an hour.

**A:** How long to wait is impossible to know, it depends entirely on the
problem you are working on. Half an hour is not unusual though.


Proof complexity
^^^^^^^^^^^^^^^^

**Q:** Does SBY, or any of the supported solvers, provide functionality to
evaluate the complexity of a proof? Or is there some hint on how to restructure
the RTL Code to simplify the problem?

**A:** We don't have anything like that currently. The question has generated a
bit of discussion on our slack for how we could estimate it - it's not easy to
correlate the activity of variables that end up in the SAT solver with anything
in the design, given the amount of rewriting that happens in the intermediate
layers. There were two suggestions that can give some proxy values that should
correlate with the complexity:

- Systematically simplifying the problem by adding assumptions that fix
  different parts of the inputs (so basically moving a slider between full proof
  and specific testcase) until things are solved quickly is probably the most
  approachable way to get some insight into solver performance for a specific
  problem.

- Using the amount of logic that is in the COI of the proof as a crude estimate
  for the complexity. We don't have a user-friendly interface for this but it
  can be done with the yosys CLI. If you have already run SBY, you can use the
  command ``yosys -p 'stat t:$assert t:$assume %ci*' <sby task
  folder>/model/design.il`` to print some statistics of the logic feeding into
  the assume and assert statements in your code (use ``'stat t:$cover t:$assume
  %ci*'`` for cover tasks). This won't take into account all of the factors that
  affect performance - e.g. deeply pipelined code, where the variable state
  depends on many previous cycles, often has particularly poor performance
  beyond what the amount of registers would suggest. (If you want to see this
  data before running SBY, open a yosys shell and run the commands from the
  ``[script]`` section before running ``'stat t:$assert t:$assume %ci*'``.)


.. Running multiple checks
.. ^^^^^^^^^^^^^^^^^^^^^^^
 
.. **Q:** Is it possible to have more than 1 liveness property check in single
.. formal run?

.. **A:** Yes, add to SBY file.
