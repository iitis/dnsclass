# namespaces
def tok(): pass
def pre(): pass

#### tokenizer
# include top-level domains?
tok.tlds = True

# segmentation threshold; 0=off
tok.seg = 0

# flow features?
tok.flow = True

# max number of tokens per domain (tokens[-max:])
if tok.flow:
    tok.max = 8
else:
    tok.max = 6

### prediction

# thresholds for feature count and decision value (>= means OK) 
if tok.flow:
    pre.F = 5
    pre.T = 0.5
else:
    pre.F = 3
    pre.T = 0.6