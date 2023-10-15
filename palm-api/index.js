const { TextServiceClient } = require("@google-ai/generativelanguage").v1beta2;
const { GoogleAuth } = require("google-auth-library");

const MODEL_NAME = "models/text-bison-001";
const API_KEY = "AIzaSyA5f0ymPLUTFl-PxkC75OPxApuUUyEYUeo";

const client = new TextServiceClient({
    authClient: new GoogleAuth().fromAPIKey(API_KEY),
});

const text = `
Making a cup of tea is easy! First, you need to get some \ 
water boiling. While that's happening, \ 
grab a cup and put a tea bag in it. Once the water is \ 
hot enough, just pour it over the tea bag. \ 
Let it sit for a bit so the tea can steep. After a \ 
few minutes, take out the tea bag. If you \ 
like, you can add some sugar or milk to taste. \ 
And that's it! You've got yourself a delicious \ 
cup of tea to enjoy.
`;

const prompt = `You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

"""${text}"""
`;

client
    .generateText({
        model: MODEL_NAME,
        prompt: {
            text: prompt,
        },
    })
    .then((result) => {
        const output = result[0]?.candidates[0]?.output;
        if (output) {
            console.log("\n", output, "\n");
        } else {
            console.log("No output available.");
        }
    });
