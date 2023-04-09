// export const prerender = false;

export const load = async ({ request }) => {
  const { headers } = request;
  const ip_country = headers.get('cf-ipcountry');
  const accept_language = headers.get('accept_language');
  
  return {
    ip_country,
    accept_language
  };
};