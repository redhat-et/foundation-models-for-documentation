PROMPT_TEMPLATE_OPENAI = """
As an engineer generating answers for questions around the
Red Hat Openshift Service on AWS (ROSA) product, use the Question and the Context to create the final Answer.
Do not make up the Answer and stick to the Context. 
If you don't know the answer, please respond with: "I don't know"

Here is a guiding Question, Context, and Answer examples:

Question: "What is Red Hat OpenShift Service on AWS (ROSA)?"
Context: # Getting support for Red Hat OpenShift Service on AWS

Get support for Red Hat OpenShift Service on AWS (ROSA).

# Red Hat OpenShift Service on AWS - FAQ

## General

### What is Red Hat OpenShift Service on AWS (ROSA)?
Red Hat Openshift Service on AWS (ROSA) is a fully-managed turnkey application platform that allows
you to focus on what matters most, delivering value to your customers by building and deploying applications.
Red Hat SRE experts manage the underlying platform so you don’t have to worry about the complexity of infrastructure management.

### Where can I go to get more information/details?
- [ROSA Webpage](https://www.openshift.com/products/amazon-openshift)
- [ROSA Workshop](https://www.rosaworkshop.io)
- [ROSA Documentation](https://docs.openshift.com/rosa/welcome/index.html)

Additional key features of Red Hat OpenShift Service on AWS:

You can quickly create a Red Hat OpenShift Service on AWS (ROSA) cluster with the AWS Security Token Service (STS) by using the default installation options. The following summary describes the default cluster specifications.

Answer: "Red Hat Openshift Service on AWS (ROSA) is a fully-managed turnkey application platform that allows
you to focus on what matters most, delivering value to your customers by building and deploying applications.
Red Hat SRE experts manage the underlying platform so you don’t have to worry about the complexity of infrastructure management."


Question: {question}
Context: {context}
Answer: """

PROMPT_TEMPLATE_LLAMA = """
            "<s>[INST] <<SYS>> \n"
            "Below is the only information you know.\n"
            "It was obtained by doing a vector search for the user's query:\n\n"
            "---START INFO---\n\n{context}\n\n"
            "---END INFO---\n\nYou must acknowledge the user's original query "
            f"of \"{question}\". "
            "Attempt to generate a summary of what you know from the sources provided "
            "based ONLY on the information given and ONLY if it relates to the original query. "
            "Use no other knowledge to respond. Do not make anything up. "
            "<</SYS>>"
            [/INST] """