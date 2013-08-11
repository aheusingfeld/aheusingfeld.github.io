module Awestruct
  module Extensions
    module ReadMore
      def truncate(content, title, url)
        index = content.index("pass::[more]")
        if index != nil
            if index > -1
                return [content[0..index-1], '<a href="', site.base_url, url, '">...read more about "', title, '"</a>']
            end
        end
        return content
      end
      def filter(content, title, url)
        index = content.index("pass::[more]")
        if index != nil
            if index > -1
                content[index..index+11]= '<a name="continue"></a>'
            end
        end
        content
      end
    end
  end
end

