<schema xmlns="http://purl.oclc.org/dsdl/schematron">
    <pattern id="shiporder">
        <rule context="shiporder">
        <assert test="@orderid">
            The orderid attribute is required.
        </assert>
        <assert test="count(orderperson)=1">
            The orderperson element is required.
        </assert>
        <assert test="count(shipto)=1">
            The shipto element is required.
        </assert>
        <assert test="count(item)>0">
            At least one item element is required.
        </assert>
        </rule>
    </pattern>
    <pattern id="item">
        <rule context="item">
        <assert test="@id">
            The id attribute is required.
        </assert>
        <assert test="count(title)=1">
            The title element is required.
        </assert>
        <assert test="count(author)=1">
            The author element is required.
        </assert>
        <assert test="count(quantity)=1">
            The quantity element is required.
        </assert>
        <assert test="count(price)=1">
            The price element is required.
        </assert>
        </rule>
    </pattern>
    <pattern id="shipto">
        <rule context="shipto">
        <assert test="count(name)=1">
            The name element is required.
        </assert>
        <assert test="count(address)=1">
            The address element is required.
        </assert>
        <assert test="count(city)=1">
            The city element is required.
        </assert>
        <assert test="count(country)=1">
            The country element is required.
        </assert>
        </rule>
    </pattern>
    <pattern id="quantity">
        <rule context="quantity">
        <assert test=". > 0">
            Item quantity must be greater than zero.
        </assert>
        </rule>
    </pattern>
</schema>
