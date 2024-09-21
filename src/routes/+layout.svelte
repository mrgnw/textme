<script>
	let {data, children} = $props()
</script>

{@render children()}

<layout>
	<pre><code>{JSON.stringify(data, null, 2)}</code></pre>
</layout>
