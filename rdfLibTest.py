from rdflib import Graph
import pprint

g = Graph()
g.parse("myDemo.nt", format="nt")

qrel = g.query(
    """
    PREFIX : <http://www.mydemo.com#>
    SELECT   ?pre_name ?next_name ?condition
    WHERE {
        
        ?s :nextstep ?p .
        ?s :treatment_name ?pre_name .
        ?s :treatment_id ?treatment_id.
        ?p :treatment_name ?next_name .
        optional{?s :treatment_conditions ?condition}
    }ORDER BY ?treatment_id

   
    """
)

for row in qrel:
    print("(%s,%s,%s)" % row)