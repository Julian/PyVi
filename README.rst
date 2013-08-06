PyVi
====


So It's a Vim Clone
-------------------

No, but it's like vim.


But It's an Editor, Right?
--------------------------

No, but you can use it to make an editor.


Uh, What?
---------

PyVi is a library implementing vim-like keybindings, along with entities like
(display-less) windows and buffers which can be embedded in other Python
applications, including an editor, for one.

Rather than every application creating vim mode keybindings from scratch, you
tell PyVi what a window corresponds to in your application, send PyVi your
keyboard input, and inspect (and likely display) the contents of the window.
