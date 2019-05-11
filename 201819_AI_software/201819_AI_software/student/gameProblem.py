
'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
# from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search

class GameProblem(SearchProblem):
    # Object attributes, can be accessed in the methods below
    MAP=None
    POSITIONS=None
    INITIAL_STATE=None
    GOAL=None
    DONE=[]
    CONFIG=None
    AGENT_START=None
    SHOPS=None
    CUSTOMERS=None
    MAXBAGS = 0
    LOAD=0
    final_state=None
    MOVES = ('West','North','East','South','Load','Unload')

   # --------------- Common functions to a SearchProblem -----------------

    def actions(self, state):
        '''Returns a LIST of the actions that may be executed in this state
        '''
        actions=[]
        pos=state[0]
        if pos[1] > 0 and (pos[0],pos[1]-1) not in self.POSITIONS['building']:
            actions.append('North')
        if pos[1] < 3 and (pos[0],pos[1]+1) not in self.POSITIONS['building']:
            actions.append('South')
        if pos[0] > 0 and (pos[0]-1,pos[1]) not in self.POSITIONS['building']:
            actions.append('West')
        if pos[0] < 9 and (pos[0]+1,pos[1]) not in self.POSITIONS['building']:
            actions.append('East')
        if pos in self.SHOPS and state[1] < self.MAXBAGS :
            actions.append('Load')
        if pos in self.CUSTOMERS and state[1] > 0 :
            actions.append('Unload')
        print('My possible actions are : '+str(actions))
        return actions

    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        pos=state[0]
        if action=='North' :
            state=((pos[0],pos[1]-1),state[1],state[2])
        if action=='South' :
            state=((pos[0],pos[1]+1),state[1],state[2])
        if action=='East' :
            state=((pos[0]+1,pos[1]),state[1],state[2])
        if action=='West' :
            state=((pos[0]-1,pos[1]),state[1],state[2])
        if action=='Load' :
            load=state[1]
            load+=max(sum([self.getPendingRequests(i) for i in self.CUSTOMERS]),self.MAXBAGS)
            state=(state[0],load,state[2])
        if action=='Unload' :
            if (state[2]<=state[1]):
                state=(state[0],state[1]-state[2],0)
            else :
                state=(state[0],0,state[2]-state[1])
        return state


    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        return state==self.GOAL

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        return 1

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        pos1 = state[0]
        pos2 = self.GOAL[0]
        if state[2]==0 : #if no pending requests, we just need to go back to the start
            cost=self.manhattan_distance(pos1,pos2)
        else : #we have pending requests
            if state[1]==self.GOAL[2]: #if we already loaded the pizzas, we need to deliver them and unload them
                cost = self.manhattan_distance(pos1,self.CUSTOMERS[0])+self.manhattan_distance(self.CUSTOMERS[0],pos2) + 1
            else : #we need to pick up pizzas first
                cost = self.manhattan_distance(pos1, self.SHOPS[0]) + self.manhattan_distance(self.SHOPS[0],self.CUSTOMERS[0]) + \
                       self.manhattan_distance(self.CUSTOMERS[0], pos2) + 2
        return cost


    def setup (self):
        '''This method must create the initial state, final state (if desired) and specify the algorithm to be used.
           This values are later stored as globals that are used when calling the search algorithm.
           final state is optional because it is only used inside the is_goal() method

           It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
        '''

        print('\nMAP: ', self.MAP, '\n')
        print('POSITIONS: ', self.POSITIONS, '\n')
        print('CONFIG: ', self.CONFIG, '\n')

        initial_state = (self.POSITIONS['start'][0],0,2)
        final_state= (self.POSITIONS['start'][0],0,0)
        algorithm= simpleai.search.astar
        #algorithm= simpleai.search.breadth_first
        #algorithm= simpleai.search.depth_first
        #algorithm= simpleai.search.limited_depth_first
        return initial_state,final_state,algorithm
        
    def printState (self,state):
        '''Return a string to pretty-print the state '''
        return str(state)

    def getPendingRequests (self,state):
        ''' Return the number of pending requests in the given position (0-N). 
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
        #if state in self.POSITIONS['customer1'] :
        #    return len(self.POSITIONS['customer1'])
        if state in self.POSITIONS['customer2'] :
            return len(self.POSITIONS['customer2'])
        return None

    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #

    def getAttribute (self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string
           
           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''
        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None

    def getStateData (self,state):
        stateData={}
        pendingItems=self.getPendingRequests(state)
        if type(pendingItems)=="<class 'int'>" :
            if pendingItems >= 0:
                stateData['newType']='customer{}'.format(pendingItems)
        return stateData
        
    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):
        self.MAP=map
        self.POSITIONS=positions
        self.CONFIG=conf
        self.AGENT_START = tuple(conf['agent']['start'])

        initial_state,final_state,algorithm = self.setup()
        if initial_state == False:
            print('-- INITIALIZATION FAILED')
            return True
      
        self.INITIAL_STATE=initial_state
        self.MAXBAGS=2
        self.SHOPS=self.POSITIONS['pizza']
        self.CUSTOMERS=self.POSITIONS['customer2']
        self.GOAL=final_state
        self.ALGORITHM=algorithm
        super(GameProblem,self).__init__(self.INITIAL_STATE)
        print('-- INITIALIZATION OK')
        return True
        
    # END initializeProblem 
