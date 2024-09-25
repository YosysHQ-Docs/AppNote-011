FAQs relating to SBY
--------------------

Documentation
^^^^^^^^^^^^^

**Q:** Where are the docs?

**A:** `SBY docs <https://yosyshq.readthedocs.io/projects/sby/en/latest/index.html>`_


SystemVerilog Assertions (SVA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** What subset of SVA is supported?

**A:** Refer to the SBY docs: `Supported SVA property syntax
<https://yosyshq.readthedocs.io/projects/sby/en/latest/verific.html#supported-sva-property-syntax>`_


Choosing an engine and solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** How do I know which formal engine and/or which solver to use for
verifying my design?

**A:** Different combinations of engine and solver will perform differently and
may support different features or functionalities.  The `SBY engines reference
<https://yosyshq.readthedocs.io/projects/sby/en/latest/reference.html#engines-section>`_
lists all currently supported engines, their options, available solvers, and
which modes they operate in.  At this time, a comprehensive comparison of when
to use different engines/solvers is not yet available.

With the introduction of the ``--autotune`` option it is now possible to
automatically compare available engines for a given SBY task.  Autotune will run
each engine, providing a report of time taken and the status returned.  This can
be used to quickly determine the fastest configuration while continuing to
iterate on a design. Check out the `autotune docs
<https://yosyshq.readthedocs.io/projects/sby/en/latest/autotune.html>`_ for more
information.

Tool runtime
^^^^^^^^^^^^

**Q:** I tried one of the examples included with the tool, and formal run looked stuck and didn't
get completed in half an hour. Not sure if engine selection has anything to do with it. How much to
wait in such case?

**A:** How long to wait is impossible to know, it depends entirely on the problem you are working
on. Half an hour is not unusual though.


Proof complexity
^^^^^^^^^^^^^^^^

**Q:** Does SBY, or any of the supported solvers, provide functionality to evaluate the complexity
of a proof? Or is there some hint on how to restructure the RTL Code to simplify the problem?

**A:** We don't have anything like that currently. The question has generated a bit of discussion on
our slack for how we could estimate it - it's not easy to correlate the activity of variables that
end up in the SAT solver with anything in the design, given the amount of rewriting that happens in
the intermediate layers. There were two suggestions that can give some proxy values that should
correlate with the complexity:

- Systematically simplifying the problem by adding assumptions that fix different parts of the
  inputs (so basically moving a slider between full proof and specific testcase) until things are
  solved quickly is probably the most approachable way to get some insight into solver performance
  for a specific problem.

- Using the amount of logic that is in the COI of the proof as a crude estimate for the complexity.
  We don't have a user-friendly interface for this but it can be done with the yosys CLI. If you
  have already run SBY, you can use the command ``yosys -p 'stat t:$assert t:$assume %ci*' <sby task
  folder>/model/design.il`` to print some statistics of the logic feeding into the assume and assert
  statements in your code (use ``'stat t:$cover t:$assume %ci*'`` for cover tasks). This won't take
  into account all of the factors that affect performance - e.g. deeply pipelined code, where the
  variable state depends on many previous cycles, often has particularly poor performance beyond
  what the amount of registers would suggest. (If you want to see this data before running SBY, open
  a yosys shell and run the commands from the ``[script]`` section before running ``'stat t:$assert
  t:$assume %ci*'``.)


Where do assertions fail
^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** How do I see what is causing my assertion to fail?

**A:** If an assertion is failing, SBY will provide a counterexample trace.
Provided you are not using the ``append`` option, the final cycle in this trace
is the cycle in which the assertion does not hold.  Check out our `quickstart
guide <https://yosyshq.readthedocs.io/projects/sby/en/latest/quickstart.html>`_
for a worked example of examining and fixing a failing assertion.

``smtbmc`` induction failures don't start from reset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** Why does the ``smtbmc`` engine in ``prove`` mode return ``FAIL`` for induction, giving a
counterexample trace that doesn't even start at reset?

**A:** The ``smtbmc`` engine uses a technique called k-induction in ``prove`` mode. This tries to
prove your design correct by checking that two facts hold:

#. Basecase: The assertions hold for the first ``depth`` cycles from reset
#. Induction: If the assertions hold for any ``depth`` cycles in a row, they also hold in the next cycle

If ``smtbmc`` can prove both of these, the assertions will always hold in the design by
the `principle of mathematical induction <https://en.wikipedia.org/wiki/Mathematical_induction>`_.
``smtbmc`` can report two types of failure for this proof, a basecase failure or an induction
failure. A basecase failure indicates a legitimate failure of the assertion found starting from
a reset state, whereas an induction failure instead just means that ``smtbmc`` was unable to establish
a complete proof. This will create a counterexample trace ``trace_induct.vcd`` that starts in an
arbitrary non-reset state and finishes by failing the assertion.

To help ``smtbmc`` prove the assertion, you can increase the ``depth`` option or add assertions
to help constrain the inductive proof. If the property is true, the states before the failure
in the induction counterexample will be states that aren't actually reachable, so adding assertions
to mark them bad helps the solver find a proof for a lower ``depth``.

Design initialisation
^^^^^^^^^^^^^^^^^^^^^

**Q:** Why does my design not get reset properly at the start?

**A:** SBY does not consider reset signals special. If you want to restrict your proof to only
certain behaviors of the reset signal, add an ``assume()`` statement enforcing the reset sequence,
e.g. ``initial assume(reset);`` (Yosys also adds the non-standard ``$initstate`` for use in
conditionals, e.g. assume property (``@(posedge clk) $initstate |-> reset [*3]);``).

Where possible we encourage writing your properties in such a way as to be able to leave the reset
signal unconstrained after the initial cycles, so as to check for bugs that might occur after a soft
reset.

Clock signals
^^^^^^^^^^^^^

**Q:** How does SBY detect and handle clock signals?

**A:** How SBY treats the clock signals differs depending on if you are using multi-clock mode
(``multiclock on`` in the ``[options]`` section) or not. In single-clock mode, the clock signal's
actual value is disregarded, we assume all registered signals update simultaneously, and the solver
has one variable per signal per clock cycle to determine. So internally, the solver will actually
never see the clock change, and we artificially add the toggling of the clock signal when generating
the trace - but that can lead to some discrepancies if there are any signals that are assigned the
value of the clock signal (such as with submodules).

In multiclock mode, the clock signal is instead treated as a regular input, and the solver can
freely choose whether to toggle it, unless you add assumptions. This means that the clock signal
will not obey the implicit rules of clock signals like having a consistent period or duty cycle, but
while surprising at first, this is actually not a disadvantage most of the time - when the clocks
are not related, it's almost always possible to eventually reach a specific interleaving of clock
edges if you let the system run long enough. Not having those constraints in place means that the
solver can find the worst case in only a few steps, giving you a short trace. With the constraints,
getting to that point might take so long that the problem becomes computationally intractable. If
your clocks are actually related, do add an assumption about that.


**Q:** When do I need to enable multi-clock mode?

**A:** You need to set ``multiclock on`` in the ``[options]`` section whenver the design contains entities that are sensitive to different events.
This includes:

- multiple clock signals
- multiple edges of the same clock signal
- any asynchronous logic (with the exception of asynchronous resets that should be treated as synchronous)

Handling combinational loops
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** SBY is failing to process my design, reporting that it has a topological logic loop even
if I don't think there is one. What can I do to allow SBY to process the design?

**A:** Formal verification tools struggle to handle combinational loops as the underlying solvers
only allow nets to take a single value per clock cycle, a property that is violated by unstable
combinational loops that oscillate. Even when you don't explicitly include a combinational loop
in the design, they can be introduced by multi-clock mode which introduces combinational
paths from clock and reset inputs to the Q output of flip-flops and from the enable input to the
output of latches.

If you are confident that a loop is only ever unstable under an unreachable condition, you can
break the loop by replacing a connection with an assumption. This forces the solvers to only
ever produce counterexamples where the loop is stable. For example, the following snippet
creates a logic loop that is unstable only when the control signals ``(sx, sy)`` are both ``0``.

.. code-block:: systemverilog

   // (sx, sy) = (0, 0) gives an unstable logic loop
   // (sx, sy) = (0, 1) gives (x, y) = (a + c + d, c + d    )
   // (sx, sy) = (1, 0) gives (x, y) = (a + b    , a + b + c)
   // (sx, sy) = (1, 1) gives (x, y) = (a + b    , c + d    )
   assign x = a + (sx ? b : y);
   assign y = c + (sy ? d : x);

To break this loop for formal verification, one of the variables in the loop can be replaced with an
``anyseq`` wire, and constrained with an assumption to take the desired value when it is known to
be stable. It is also a good idea to add an assertion checking that the conditions leading to an
unstable loop cannot happen. Note that even with this assertion, if unstable loops can occur in other
cases the design could suffer from `overconstraint due to assumptions`_.

.. code-block:: systemverilog

   `ifdef FORMAL
     // Define the conditions when we know the loop will be unstable. At all other
     // times it is assumed to be stable which can hide counterexamples so care must be
     // taken. We use an assertion to make sure the unstable condition can never be seen.
     wire loop_unstable;
     assign loop_unstable = {sx, sy} == '0;
     always @* assert(!loop_unstable);

     // Break the loop through x using an assumption when the loop is known to be stable
     (* anyseq *) wire x;
     always @* begin
       if (!loop_unstable)
         assume(x == a + (sx ? b : y)); 
     end
   `endif

If the loop is introduced through a latch by multi-clock mode, sometimes the latch can be safely
replaced with a flip-flop which doesn't have the same combinational paths. The standard clock-gating
pattern shown below is an example of a circuit amenable to this technique.

.. code-block:: systemverilog

   module clock_gate(input wire clk_i, input wire en_i, output wire gated_clk_o);
   // Latch means that en_l only changes when clk_i is low, so gated_clk_o cannot glitch
   reg en_l;
   always @* begin
     if (!clk_i)
       en_l = en_i;
   end

   assign gated_clk_o = en_l & clk_i;
   endmodule

For formal verification an alternate version of this module can be used where
a flip-flop is used to rewrite the design without the same combinational paths
in multi-clock mode.

.. code-block:: systemverilog

   module clock_gate(input wire clk_i, en_i, output wire gated_clk_o);
   reg en_r;
   always @(posedge clk_i)
     en_r <= en_i;

   assign gated_clk_o = en_r && clk_i;
   endmodule

Semantics of "disable iff"
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** I would have expected the following to pass. Why does it not pass?

.. code-block:: systemverilog

   assume property (@(posedge clock) A |-> B disable iff (reset));
   assert property (@(posedge clock) A && !reset |-> B );

**A:** Both of those properties are two simulation cycles long, because the
clock edge between those two cycles is part of the property. The ``disable iff``
statement behaves similar to an *asynchronous* reset that is not sampled
by the clock, thus the sequence ``A && !B && !reset ##1 reset`` will disable
the assumption, but will not disable the assertion in the above example.

Overconstraint due to assumptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** Is it possible for assumptions to hide counterexamples even when they do not share
any logic with assertions?

**A:** Yes, if all counterexamples to the assertions also violate the assumptions they
would be hidden. This normally happens if the assumptions make it impossible for the design
to progress without violating them meaning assertions can vacuously pass even though they
can never be witnessed to hold. `Witness cover traces`_ can be used to try to guard against
this type of failure, but care should be taken when applying assumptions, preferring
assumptions on top-level I/O over internal signals. An extreme example of overconstraint
would be a design that fails the `PREUNSAT check`_.

PREUNSAT check
^^^^^^^^^^^^^^

**Q:** Can SBY detect when assumptions prevent any progress for the design?

**A:** The ``smtbmc`` engine is able to perform ``PREUNSAT`` checks for each
bound. These check that there is at least one trace of that length that obeys
all of the assumptions. Failure of the ``PREUNSAT`` check is clear evidence of
overconstraint, however there are many cases of overconstraint it is unable
to catch. For example, if the design is able to stall indefinitely in one state,
this allows arbitrary length traces so PREUNSAT will pass even if the design is
subsequently overconstrained.

Witness cover traces
^^^^^^^^^^^^^^^^^^^^

**Q:** How do I produce witness cover traces for a passing assertion?

**A:** Check out the `witness cover section
<https://yosyshq.readthedocs.io/projects/ap120/en/latest/#witness-cover>`_ of our
whitepaper, `Weak precondition cover and witness for SVA properties
<https://yosyshq.readthedocs.io/projects/ap120>`_.

.. Running multiple checks
.. ^^^^^^^^^^^^^^^^^^^^^^^
 
.. **Q:** Is it possible to have more than 1 liveness property check in single formal run?

.. **A:** Yes, add to SBY file.

Can liveness properties fail
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
**Q:** Is it possible to have liveness property to fail? Or will it just get stuck in formal run 

**A:** We don't recommend using liveness properties - it's almost always better to replace with an
assertion of something happening within a certain timeframe.

The example our CTO gives is of a design that is stuck in a deadlock, but it has a 64 bit counter
and when that overflows, things start up again. Liveness will tell you "yup, this design will do
things eventually" but it really doesn't help you because that 64 bit counter is so large that your
design will basically never start again.
