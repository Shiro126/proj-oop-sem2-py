## We need some cool rules to make our lives easier

#### Git 
1. Each new feature you develop should be at first pushed into a **new branch** like this:

`git branch <my_cool_feature_branch>`

*\*here the work happens*\*

`git add -A; git commit -m "my cool commit"`

`git push --set-upstream origin <my_cool_feature_branch>`
  #
  **origin** means the remote repo adress, if you want to know more, watch some git tutorials or ask Bączek.
  **<my_cool_feature_branch>** is the title of your branch
  # 
2.  After that, check if you can merge your branch with **master** branch and if you're sure that there will be no problems, merge it into master.
3.  If you are not sure, ask the team what they think.
4.  After merging you can delete your local branch like this:

`git checkout master` - jump back into **master** so you can delete the branch you were on

`git branch -d <my_cool_feature_branch>` - **<my_cool_feature_branch>** being the name of your branch.

5. Test how are things going on the **master** branch after merging.

# 
#### Code
1. **Write. More. Comments.**
2. [Learn how docstrings work in python](https://www.python.org/dev/peps/pep-0257/) (come on, PyCharm does 90% of autocompletion for you, there is not much to learn and people will be happy if you write docstrings).
3. Write functions for things that you use repeatedly.
 



