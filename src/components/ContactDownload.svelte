<script>
    import { Contact } from 'lucide-svelte';
    const { phone } = $props();
  
    function generateVCard() {
      // Remove any non-numeric characters and ensure it starts with a +
      const cleanPhone = phone.replace(/[^\d]/g, '');
      const formattedPhone = cleanPhone.startsWith('+') ? cleanPhone : `+${cleanPhone}`;
      
      const vcard = [
        'BEGIN:VCARD',
        'VERSION:3.0',
        'FN:Contact',  // We could make this configurable if needed
        `TEL;TYPE=CELL:${formattedPhone}`,
        `TEL;TYPE=WHATSAPP:${formattedPhone}`,
        `X-SOCIALPROFILE;TYPE=telegram:https://t.me/${formattedPhone}`,
        'END:VCARD'
      ].join('\n');
  
      return vcard;
    }
  
    function downloadVCard() {
      const vcard = generateVCard();
      const blob = new Blob([vcard], { type: 'text/vcard' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'contact.vcf';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    }
  </script>
  
  <!-- Add this near your existing contact buttons -->
  <button 
    class="download-contact-btn"
    on:click={downloadVCard}
    aria-label="Download contact card">
    <Contact size={20} /> Save Contact
  </button>
  
  <style>
    .download-contact-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
  </style>