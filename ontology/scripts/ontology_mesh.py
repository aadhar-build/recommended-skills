import os
import yaml
import re

class OntologyMesh:
    def __init__(self, base_dir="vault/_ontology"):
        self.base_dir = base_dir

    def generate_mermaid_graph(self):
        """Generates a Mermaid graph string from Ontology YAML frontmatter."""
        graph = ["graph TD"]
        entities_dir = os.path.join(self.base_dir, "entities")
        
        if not os.path.exists(entities_dir):
            return ""

        for file in os.listdir(entities_dir):
            if file.endswith(".md"):
                name = file.replace(".md", "")
                path = os.path.join(entities_dir, file)
                with open(path, 'r') as f:
                    content = f.read()
                    # Extract YAML frontmatter
                    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                    if match:
                        try:
                            data = yaml.safe_load(match.group(1))
                            relates = data.get('relates_to', [])
                            if isinstance(relates, list):
                                for link in relates:
                                    clean_link = str(link).replace("[[", "").replace("]]", "")
                                    graph.append(f"    {name} --> {clean_link}")
                        except Exception as e:
                            print(f"Error parsing {file}: {e}")
        
        return "\n".join(graph)

if __name__ == "__main__":
    om = OntologyMesh()
    print(om.generate_mermaid_graph())
