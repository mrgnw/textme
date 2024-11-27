<script>
	/** @type {{value?: any, detailedValue?: any, cf_data?: any}} */
	let { value = null, detailedValue = null, cf_data = null } = $props();
</script>

<pre><code>{JSON.stringify(value, null, 2)}</code></pre>
<pre><code>{JSON.stringify(detailedValue, null, 2)}</code></pre>
<pre><code>{JSON.stringify(cf_data, null, 2)}</code></pre>