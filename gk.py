from dataclasses import dataclass
import numpy as np
from typing import List, Union

@dataclass
class Item:
    value: float
    g: int
    delta: int

class Sketch:
    def __init__(self, eps) -> None:
        self.eps = eps
        self.N = 0
        self.items = []

    def merge(self) -> None:
        i = len(self.items)-1 #we begin check from pre-last element, as we always need to preserve min and max
        while i > 1:
            j = i - 1
            g_sum = self.items[i].g
            while j > 0 and g_sum + self.items[j].g + self.items[i].delta < 2*self.eps*self.N:
                g_sum += self.items[j].g
                j -= 1
            
            # loop ends if be reach first element or error of interval becomes too big to compress
            # this is why we return back to one element where interval is still replacable
            j += 1
            if j < i:
                new_item = Item(self.items[i].value, g_sum, self.items[i].delta)
                self.items = self.items[:j] + [new_item] + self.items[i+1:]
            i = j-1
    
    def insert(self, val: float) -> None:
        d = 0
        idx = len(self.items)
        for i in range(0, len(self.items)):
            if val < self.items[i].value:
                idx = i
                break
        
        d = 0 if idx == 0 or idx == len(self.items) else self.items[idx].g + self.items[idx].delta - 1
        self.items.insert(idx, Item(val, 1, d))
        self.N += 1
        if self.N % int(1/(2*self.eps)) == 0:
            self.merge()
        
        
    def quantile(self, q:float):
        rank = int(q*self.N)
        rmin = 0
        for i in range(1, len(self.items)):
            rmin += self.items[i-1].g
            if rmin + self.items[i].g + self.items[i].delta > rank+int(self.eps*self.N):
                return self.items[i-1].value
        
        return self.items[len(self.items)-1].value
    
    def items_num(self) -> int:
        return len(self.items)