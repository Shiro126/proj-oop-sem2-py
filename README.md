## Stuff you could do

#### Feel free to edit this file and add your own ideas
Just remember to note that a task is assigned to you
#
##### Saving the net weights values to a JSON file
1. `save_to _json(filename)` - saves net weights and stores it in the `filename` location.
2. `load_from_json(filename)` - loads the net weights from `filename`
3. `protip:` save the network parameters in the json file, so when you load it you will know how to construct your network before you load weights to it.

*Assigned to Wiesiołek*
#
##### Alternate way of feeding information into the network
Currently we're giving the coordinates to the net.
I have [another idea](https://youtu.be/BBLJFYr7zB8), skip to 30s to see what i'm talking about.

*Not assigned yet*

#
##### Some kind of command line interface..?
I'm talking:
You start the program, a menu inside the console appears:

```
0. Test vs dummy
1. Train network visible (from the start)
2. Train network visible (load net from file)
3. Train network super-fast-invisible (from the start)
4. Train network super-fast-invisible (load net from file)
5. Show saved networks
6. Play with a saved neural network
7. Deploy battle drones and assasinate somebody (just kidding FBI)
```

*Not assigned yet*

#
##### Create a better logging mechanism than `print`
[Maybe we should use this](https://docs.python.org/3/library/logging.html)

Let's avoid printing million of lines every time we try to just run the app.
It looks pretty messy currently.

*Not assigned yet*

#
##### Move the neural network implementation away from the NeuralController class
You see, NeuralController is getting bigger and bigger, meanwhile a neural network 'module' could be re-used..
(for example, if you'd want to change the way plane responds to the NN outputs, you would copy the whole class, then change the predict method a bit, if you could just put the NeuralNetwork inside the different PlaneController classes, it would make the whole thing more modular).

So... Let's move the Neural Net implementation to a dedicated class so that we can use it inside many controllers via composition!

*Not assigned yet*

#
#### Your ideas are welcomed. So you better write them below
