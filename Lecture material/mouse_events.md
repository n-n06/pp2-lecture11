# Mouse events
## Keyboard events
You already know how to access keyboard events. There are 2 main methods:
- Event queue
- get_pressed() method of key module

### Event queue
```python
...
flLeft = flRight = False #flags for left and right movement
while True:
    ...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                flLeft = True
            elif event.key == pygame.K_RIGHT:
                flRight = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                flLeft = flRight = False
    ...
    if flLeft:
        x -= 5
    elif flRIght:
        x += 5
    ...
```
When using this method, we check every Event object in the pygame's event queue.
When we are interested in a key being *pressed*, we use `pygame.KEYDOWN`.  
We can also check if a key is *released* using `pygame.KEYUP`.  
In the example above (it is from one of the previous lectures), we change some object's position when the left or right arrow keys are pressed. 


### get_pressed() method
```python
while True:
    ...
    pressed = pygame.key.get_pressed()
    alt = pressed_key[pygame.K_LALT] or pressed_key[pygame.K_RALT]
    ctrl = pressed_key[pygame.K_LCTRL] or pressed_key[pygame.K_RCTRL]
```
In this example we access `pygame.key.get_pressed()` function that return a dictionary that contains **keys** as, well, keys and **bool values** as the values.  
So, `ctrl` variable contains either `True` or `False` value depednding on whether the left ctrl or right ctrl buttons were pressed.  

## What about the mouse? It is almost the same!
### Event queue
**We have 4 types of events for mouse**
```python
pygame.MOUSEBUTTONDOWN
pygame.MOUSEBUTTONUP
pygame.MOUSEMOTION
pygame.MOUSEWHEEL
```
  
> Let's look closer at `pygame.MOUSEBUTTONDOWN`:
This event tracks whether mousebuttons are pressed or the wheel is scrolled.  
```python
...
while True:
    ...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Pressed button: ", event.button)

...
```
Here we simply access the button paramater of a mouse event. Its values are:  
1 - left mouse button  
2 - middle mouse button  
3 - right mouse button  
4 - scroll up  
5 - scroll down  

> `pygame.MOUSEMOTION`  
This type of event track mouse motion.  
This event has 2 important parameters: `event.pos` - mouse position, and `event.rel` - mouse position relative to the previous one
```python
...
while True:
    ...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEMOTION:
            print("Absolute position: ", event.pos)
            print("Relative position: ", event.rel)
...

```
> `pygame.MOUSEWHEEL`  
Can be used to track the movement of the wheel.  
Has a useful attribute - `dict` where the information about the wheel is stored  
We can access the movement of the scroll button as follows:
```python
...
while True:
    ...
    for event in pygame.event.get():
        ...
        if event.type == pygame.MOUSEWHEEL:
            print(event.dict["y"], event.dict["precise_y"])
```
In this code, we access the `"y"` and `"precise_y"` values from the event's dict paramter.  
These parameter represent the movement of the scroll button where numbers > 0 represent scrolling up and numbers < 0 represent scrolling down

## pygame.mouse
We can use this method of accessing the mouse events in order to solve one issue with the event queue method:  
When, for example, a mouse button down event is activated, it is activated only once. In other words, if we hold the mouse button, the code block after the condition will be executed only once.

To solve this, we can use pygame's `mouse` module. In particular, the `get_pressed()` function.  
This function return a tuple of the type: `(True,False,False)` where True corresponds to a mouse button being pressed and False - to not being pressed.
```python
...
while True:
    ...
    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        print("Pressed button : 1")
...
```
