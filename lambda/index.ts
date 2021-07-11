// index.ts
const MESSAGE = {
  message: "Automate all the things!",
  secretMessage: "Automation for the people!",
  timestamp: Math.round(Date.now() / 1000),
};
const RESPONSE = {
  statusCode: 200,
  body: JSON.stringify(MESSAGE),
  isBase64Encoded: false,
};
export async function main(event: any, context: any) {
  console.log(RESPONSE);
  return RESPONSE;
}
