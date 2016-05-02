Updating more than one at a time!
---
```
# So since Elon is pretty much the most amazing human in the world he wants to update
# his name to Elon Musk The Great. Alongside of that I decided that I want to update 
# my age to 27. The best way to perform more than one action at a time in elasticsearch
# is through the bulk API. In my repository there is the bulk.json file.

curl -XPOST http://localhost:9200/_bulk?pretty=true --data-binary @bulk.json
```

Reference
---
https://github.com/andrewpuch/elasticsearch_examples
