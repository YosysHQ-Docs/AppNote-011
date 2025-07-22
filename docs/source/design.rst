Design setup FAQs
-----------------

.. Includes/defines
.. ^^^^^^^^^^^^^^^^

.. TODO


SystemVerilog Assertions (SVA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** What subset of SVA is supported?

**A:** Refer to the SBY docs: :external+sby:ref:`supported sva property syntax`.


SVA+VHDL
^^^^^^^^

**Q:** Can I use a VHDL design with properties written in SVA?

**A:** Refer to the SBY docs: :external+sby:ref:`sva properties in a vhdl
design`.


Blackboxing
^^^^^^^^^^^

**Q:** How do I blackbox a submodule to make SBY run faster?  I tried to use the
:external+yosys:doc:`blackbox command <cmd/blackbox>` but then it raises an
error. 

**A:** Many of the Yosys commands needed for SBY do not support blackbox
modules.  However, it is possible to use the :external+yosys:doc:`cutpoint
command <cmd/cutpoint>` to disconnect a module's inputs and drive its outputs
with ``$anyseq`` cells which the solver can assign any value to at each step.
This then allows the module to be verified independently of the rest of the
design.

If your design already contains blackbox modules, you can use ``cutpoint
-blackbox`` to replace all instances of blackboxes with a formal cut point.

**Q:** Is it possible to blackbox all multipliers in a design?

**A:** Yes!  Calling ``cutpoint t:$mul`` after loading the design will add
cutpoints for all cells of type ``$mul``, i.e. all of the multipliers.
