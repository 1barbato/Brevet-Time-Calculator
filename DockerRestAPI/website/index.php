<html>
    <head>
        <title>CIS 322 REST-api demo: Laptop list</title>
    </head>

    <body>
        <h1>Consumer Program</h1>
        <ul>
            <?php
            function getData($endpoint) {
                $response = file_get_contents('http://laptop-service:5000' . $endpoint);
                if ($response === False) {
                    die('Oops');
                }
                if (strpos($endpoint, 'csv') !== False){
                    return $response;
                }
                return json_decode($response, true);
            }

            $listAll = getData('/ListAll');
            $listAlljson = getData('/ListAll/json?top=2');
            $listAllcsv = getData('/ListAll/csv');
            $listOpenOnly = getData('/ListOpenOnly');
            $listOpenOnlyjson = getData('/ListOpenOnly/json');
            $listOpenOnlycsv = getData('/ListOpenOnly/csv?top=1');
            $listCloseOnly = getData('/ListCloseOnly?top=3');
            $listCloseOnlyjson = getData('/ListCloseOnly/json');
            $listCloseOnlycsv = getData('/ListCloseOnly/csv');
            ?>
        </ul>
        <h1>List All</h1>
        <pre><?php print_r($listAll); ?></pre>
        <h2>json + top 2</h2>
        <pre><?php print_r($listAlljson); ?></pre>
        <h2>csv</h2>
        <pre><?php print_r($listAllcsv); ?></pre>
        <h1>List Open Only</h1>
        <pre><?php print_r($listOpenOnly); ?></pre>
        <h2>json</h2>
        <pre><?php print_r($listOpenOnlyjson); ?></pre>
        <h2>csv + top 1</h2>
        <pre><?php print_r($listOpenOnlycsv); ?></pre>
        <h1>List Close Only</h1>
        <h2> + top 3</h2>
        <pre><?php print_r($listCloseOnly); ?></pre>
        <h2>json</h2>
        <pre><?php print_r($listCloseOnlyjson); ?></pre>
        <h2>csv</h2>
        <pre><?php print_r($listCloseOnlycsv); ?></pre>

    </body>
</html>
